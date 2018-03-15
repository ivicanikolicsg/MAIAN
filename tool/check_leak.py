from __future__ import print_function
from parse_code import *
from values import get_params, set_params, initialize_params, print_params, MyGlobals, clear_globals
from execute_block import *  
from blockchain import *



def ether_leak( op, stack, trace, debug ):

    global s
    
    # CALL leaks
    if op == 'CALL' and len(stack) >= 7 and stack[-2]['type'] == 'constant' and stack[-3]['type']=='constant':
        MyGlobals.s.push()
        MyGlobals.s.add( stack[-2]['z3'] == BitVecVal( int( get_params('my_address',''), 16), 256) )        # CALL sent address coincides with our address
        MyGlobals.s.add( stack[-3]['z3'] > 0)                                                               # amount of Ether sent is > 0
        try:
            if MyGlobals.s.check() == sat:

                # Search condition found but keep expanding the search tree to make sure that the execution ends normally,
                # i.e. with STOP/RETURN/SUICIDE
                return True, False

        except Exception as e:
            print ("Exception: "+str(e))

        MyGlobals.s.pop()


    # SUICIDE leaks
    if op == 'SUICIDE' and len(stack) >= 1 and stack[-1]['type'] == 'constant':

        MyGlobals.s.push()
        MyGlobals.s.add( stack[-1]['z3'] == BitVecVal( int( get_params('my_address',''), 16), 256) )        # SUICIDE send address coincides with our address
        
        try:
            if MyGlobals.s.check() == sat:

                # Once SUICIDE is executed, then no need to look for the final STOP or RETURN
                # because SUICIDE is already a stopping instruction
                global stop_search
                MyGlobals.stop_search = True
                
                return True, True

        except Exception as e:
            print ("Exception: "+str(e))

        MyGlobals.s.pop()

    return False, False


def run_one_check( max_call_depth, ops, contract_address, debug, read_from_blockchain ):

    global MAX_CALL_DEPTH

    print('\n[ ]\033[1m Search with call depth: %d   : \033[0m' % (max_call_depth) , end = '')


    initialize_params(read_from_blockchain, contract_address )
    clear_globals()

    # The amount of sent Ether to the contract is zero
    set_params( 'call_value', '','0'  )

    MyGlobals.MAX_CALL_DEPTH    = max_call_depth

    storage = {}    
    stack   = []
    mmemory = {}
    data = {}
    trace   = []
    configurations = {}

    execute_one_block(ops,stack,0, trace, storage, mmemory, data, configurations,  ['CALL','SUICIDE'], ether_leak, 0, 0, debug, read_from_blockchain )



def check_one_contract_on_ether_leak(contract_bytecode, contract_address, debug = False, read_from_blockchain = False, confirm_exploit=False, fhashes=[] ):


    print('\033[94m[ ] Check if contract is PRODIGAL\033[0m\n')
    print('[ ] Contract address   : %s' % contract_address)
    print('[ ] Contract bytecode  : %s...' % contract_bytecode[:50])
    print('[ ] Bytecode length    : %d' % len(contract_bytecode) )
    print('[ ] Blockchain contract: %s' % confirm_exploit)
    print('[ ] Debug              : %s' % debug)



    ops = parse_code( contract_bytecode, debug )
    if not code_has_instruction( ops, ['CALL','SUICIDE']) :
        #if debug: 
        print('\033[92m[+] The code does not have CALL/SUICIDE, hence it is not prodigal\033[0m')
        return False
    if debug: print_code( contract_bytecode, ops )

    #
    # Search for function invocations (from 1 to max_calldepth) that can make the contract to leak Ether
    #

    for i in range( 1 , MyGlobals.max_calldepth_in_normal_search + 1 ):
        run_one_check( i, ops, contract_address, debug, read_from_blockchain )

        if MyGlobals.stop_search: 
            break

    if MyGlobals.stop_search: 

        print('\n\n\033[91m[-] Leak vulnerability found! \033[0m\n\n    The following %d transaction(s) will trigger the contract to leak:' % MyGlobals.no_function_calls )

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
            
            print('\033[1m[ ] Confirming leak vulnerability on private chain ... \033[0m', end='' )

            txs = []

            for n in range(MyGlobals.no_function_calls):

                tx = {}
                tx['from'] = '0x' + MyGlobals.adversary_account
                tx['to'] = contract_address
                tx['value'] = MyGlobals.function_calls[n+1]['value']
                tx['data'] = '0x' + MyGlobals.function_calls[n+1]['input']

                txs.append(tx)

            adversary_ether_before = MyGlobals.web3.eth.getBalance('0x' + MyGlobals.adversary_account)

            weiused = execute_transactions( txs) 

            difference_in_wei = MyGlobals.web3.eth.getBalance('0x' + MyGlobals.adversary_account) + weiused - adversary_ether_before

            if difference_in_wei > 0:
                print('\n    \033[1m\033[91mConfirmed ! The contract is prodigal !\033[0m')
            else:
                print('\033[94m    Cannot confirm the leak vulnerability \033[0m')
                
        else:
            print('\033[94m[-] Cannot confirm the bug because the contract is not deployed on the blockchain.\033[0m')


        return True


    print('\n\033[92m[+] No prodigal vulnerability found \033[0m')
    return False




    