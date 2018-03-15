from __future__ import print_function
from parse_code import *
from values import get_params, set_params, initialize_params, print_params, MyGlobals, clear_globals
from execute_block import *  
from blockchain import *


def ether_suicide( op, stack, trace, debug ):

    # Once SUICIDE is executed, the contract is killed
    # Thus the search is stoppped and the contract is flagged as suicidal
    global stop_search
    MyGlobals.stop_search = True

    return True, True


def run_one_check( max_call_depth, ops, contract_address, debug, read_from_blockchain ):


    print('\n[ ]\033[1m Search with call depth: %d   : \033[0m' % (max_call_depth) , end = '')


    initialize_params(read_from_blockchain, contract_address )
    clear_globals()

    global MAX_CALL_DEPTH
    MyGlobals.MAX_CALL_DEPTH    = max_call_depth

    storage = {}    
    stack   = []
    mmemory = {}
    data = {}
    trace   = []
    configurations = {}

    execute_one_block(ops,stack,0, trace, storage, mmemory, data, configurations,  ['SUICIDE'], ether_suicide, 0, 0, debug, read_from_blockchain )




def check_one_contract_on_suicide(contract_bytecode, contract_address, debug, read_from_blockchain, confirm_exploit=False, fhashes=[] ):

    print('\033[94m[ ] Check if contract is SUICIDAL\033[0m\n')
    print('[ ] Contract address   : %s' % contract_address)
    print('[ ] Contract bytecode  : %s...' % contract_bytecode[:50])
    print('[ ] Bytecode length    : %d' % len(contract_bytecode) )
    print('[ ] Blockchain contract: %s' % confirm_exploit)
    print('[ ] Debug              : %s' % debug)



    ops = parse_code( contract_bytecode, debug )
    if not code_has_instruction( ops, ['SUICIDE']) :
        #if debug: 
        print('\n\033[92m[-] The code does not contain SUICIDE instructions, hence it is not vulnerable\033[0m')
        return False
    if debug: print_code( contract_bytecode, ops )


    # Make the amount of sent Ether symbolic variable (i.e., it can take any value)
    global symbolic_vars
    MyGlobals.symbolic_vars = ['CALLVALUE']

    #
    # Search for function invocations (from 1 to max_calldepth) that can make the contract the be killed
    #
    for i in range( 1 , MyGlobals.max_calldepth_in_normal_search + 1 ):
        run_one_check( i, ops, contract_address, debug, read_from_blockchain )

        if MyGlobals.stop_search: 
            break


    if MyGlobals.stop_search:

        print('\n\n\033[91m[-] Suicidal vulnerability found! \033[0m\n\n    The following %d transaction(s) will trigger the contract to be killed:' % MyGlobals.no_function_calls )

        for n in range(MyGlobals.no_function_calls):
            print('    -Tx[%d] :' % (n+1), end='' ) 
            for j in range(len(MyGlobals.function_calls[n+1]['input'] )):
                if (j-8) % 64 == 0: print(' ',end='')
                print('%s' % MyGlobals.function_calls[n+1]['input'][j], end='')
            print('') 

        if len(fhashes) > 0:
            print('\n    The transactions correspond to the functions:')
            for n in range(MyGlobals.no_function_calls):
                if MyGlobals.function_calls[n+1]['input'][:8] in fhashes:
                    print('    -'+fhashes[ MyGlobals.function_calls[n+1]['input'][:8] ])
            print()

        if confirm_exploit:
            
            print('\033[1m[ ] Confirming suicide vulnerability on private chain ... \033[0m', end='' )


            txs = []

            for n in range(MyGlobals.no_function_calls):

                tx = {}
                tx['from'] = '0x' + MyGlobals.adversary_account
                tx['to'] = contract_address
                tx['value'] = MyGlobals.function_calls[n+1]['value']
                tx['data'] = '0x' + MyGlobals.function_calls[n+1]['input']

                txs.append(tx)

            execute_transactions( txs) 

            bcod = MyGlobals.web3.eth.getCode(contract_address)
            if len(bcod) <= 2:
                print('\n    \033[1m\033[91mConfirmed ! The contract is suicidal !\033[0m')
            else:
                print('\033[94m    Cannot confirm the suicide vulnerability \033[0m')
                
        else:
            print('\033[94m[-] Cannot confirm the bug because the contract is not deployed on the blockchain.\033[0m')

        return True


    print('\n\033[92m[-] No suicidal vulnerability found \033[0m')


    return False






