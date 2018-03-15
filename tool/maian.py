'''
Copyright (c) 2018, Ivica Nikolic <cube444@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from __future__ import print_function
from web3 import Web3, KeepAliveRPCProvider, IPCProvider
import argparse,subprocess,sys


found_depend = False
try:
    import z3
except:
    print("\033[91m[-] Python module z3 is missing.\033[0m Please install it (check https://github.com/Z3Prover/z3)")
    found_depend = True
try:
    import web3
except:
    print("\033[91m[-] Python module web3 is missing.\033[0m Please install it (pip install web3).")
    found_depend = True

if not (subprocess.call("type solc", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0):
    print("\033[91m[-] Solidity compiler is missing.\033[0m Please install it (check http://solidity.readthedocs.io/en/develop/installing-solidity.html) and make sure solc is in the path.")
    found_depend = True

if not (subprocess.call("type geth", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0):
    print("\033[91m[-] Go Ethereum is missing.\033[0m Please install it (check https://ethereum.github.io/go-ethereum/install/) and make sure geth is in the path.")
    found_depend = True

if found_depend:
    sys.exit(1)



import check_suicide 
import check_leak 
import check_lock
from values import MyGlobals
from blockchain import *
from contracts import *


global debug, max_calldepth_in_normal_search, read_from_blockchain, checktype


def main(args):


    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--check",        type=str,   help="Check type: use 0 for SUICIDAL check, 1 for PRODIGAL, and 2 for GREEDY", action='store')
    parser.add_argument("-s","--soliditycode", type=str,   help="Check solidity contract by specifying: 1) contract file, 2) Main contract name ", action='store', nargs=2)
    parser.add_argument("-b","--bytecode",        type=str,   help="Check compiled bytecode contract by specifying contract file", action='store')
    parser.add_argument("-bs","--bytecode_source",        type=str,   help="Check source bytecode contract by specifying contract file", action='store')
    parser.add_argument("--debug",        help="Print extended debug info ", action='store_true')
    parser.add_argument("--max_inv",        help="The maximal number of function invocations (default 3) ", action='store')
    parser.add_argument("--solve_timeout",        help="Z3 solver timeout in milliseconds (default 10000, i.e. 10 seconds)", action='store')

    args = parser.parse_args( args )


    if args.debug:          MyGlobals.debug = True
    if args.max_inv:        MyGlobals.max_calldepth_in_normal_search = int(args.max_inv)
    if args.solve_timeout:  MyGlobals.SOLVER_TIMEOUT = int(args.solve_timeout)
    if args.check:          MyGlobals.checktype = int(args.check)


    kill_active_blockchain()


    if args.soliditycode or args.bytecode_source:

        print('\n'+'=' * 100)

        read_from_blockchain = True


        # First compile the contract and produce bytecode/abi
        fhashes = {}
        if args.soliditycode:
            compile_contract(args.soliditycode[0])
            contract_code_path = 'out/'+args.soliditycode[1]+'.bin'
            if not os.path.isfile( contract_code_path ):  
                print('\033[91m[-] Contract %s does NOT exist\033[0m' % args.soliditycode[1] )
                return

            # Get the contract function hashes (used later if the contract has vulnerability)
            fhashes = get_function_hashes( args.soliditycode[1] )

        # Connect (start) the private blockchain
        start_private_chain('emptychain',MyGlobals.etherbase_account)

        # If check on leak then we need to send Ether to the contract address before deploying it
        # This helps later to verify that the contract leaks Ether
        # Sending Ether has to be done prior to deployment of contract because the contract code may not allow arbitrary account to send Ether
        if 1 == MyGlobals.checktype:    
            supposed_contract_address = predict_contract_address(MyGlobals.etherbase_account)
            print('\033[1m[ ] Sending Ether to contract %s  \033[0m' % supposed_contract_address, end='')            
            execute_transactions([{'from':'0x'+MyGlobals.sendingether_account,'to':supposed_contract_address,'value':MyGlobals.send_initial_wei}])
            print('\033[92m Sent! \033[0m')

        # Deploy the contract
        if args.soliditycode:   contract_address = deploy_contract(args.soliditycode[1], MyGlobals.etherbase_account)
        else:                   contract_address = deploy_contract(args.bytecode_source, MyGlobals.etherbase_account, True)

        if contract_address is None:
            print('\033[91m[-] Cannot deploy the contract \033[0m' )
            return


        # If check on leak, then make sure the contract has Ether
        if 1 == MyGlobals.checktype:
            bal = MyGlobals.web3.eth.getBalance(contract_address)
            print('\033[1m[ ] The contract balance: %d  \033[0m' % bal, end='' )
            if bal > 0:
                print('\033[92m Positive balance\033[0m')
            else:
                print('cound not send Ether to contract')
                return 


        code = MyGlobals.web3.eth.getCode(contract_address)
        if code[0:2] == '0x': code = code[2:]

        if 0 == MyGlobals.checktype: ret = check_suicide.check_one_contract_on_suicide(code, contract_address, MyGlobals.debug, MyGlobals.read_from_blockchain, True, fhashes)
        elif 1== MyGlobals.checktype: ret = check_leak.check_one_contract_on_ether_leak(code, contract_address, MyGlobals.debug, MyGlobals.read_from_blockchain, True, fhashes)
        elif 2== MyGlobals.checktype: ret =  check_lock.check_one_contract_on_ether_lock(code, contract_address, MyGlobals.debug, MyGlobals.read_from_blockchain)

        kill_active_blockchain()

        
    elif args.bytecode:

        print('\n'+'=' * 100)

        read_from_blockchain = False
        filepath_code = args.bytecode
        if not os.path.isfile(filepath_code):  
            print('\033[91m[-] File %s does NOT exist\033[0m' % filepath_code )
            return

        with open(filepath_code,'r') as f: code = f.read(); f.close()
        code = code.replace('\n','').replace('\r','').replace(' ','')
        if code[0:2] == '0x': code = code[2:]

        if 0 == MyGlobals.checktype:        ret = check_suicide.check_one_contract_on_suicide(code, '', MyGlobals.debug, MyGlobals.read_from_blockchain, False)
        elif 1 == MyGlobals.checktype:  ret = check_leak.check_one_contract_on_ether_leak(code, '', MyGlobals.debug, MyGlobals.read_from_blockchain, False)
        elif 2 == MyGlobals.checktype:  ret =  check_lock.check_one_contract_on_ether_lock(code, '', MyGlobals.debug, MyGlobals.read_from_blockchain)




    else:
        pass





if __name__ == '__main__':

    global exec_as_script 
    MyGlobals.exec_as_script = True
    import sys
    main(sys.argv[1:])
