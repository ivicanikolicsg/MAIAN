from __future__ import print_function
from parse_code import *
from values import get_params, set_params, initialize_params, print_params, MyGlobals, clear_globals
from execute_block import *  


def ether_lock_can_recieve( op, stack, trace, debug ):

    # Once STOP/RETURN  is executed, the search can be stoppped
    global stop_search
    MyGlobals.stop_search = True

    return True, True


def ether_lock_can_send( op, stack, trace, debug ):


    # Once one of the instructions that can send Ether is reached, then the search can be stoppped

    # If terminating instruction SUICIDE, the can stop the further search
    if op in ['SUICIDE']:
        global stop_search
        MyGlobals.stop_search = True
        return True, True
    # When the op is one among CALL,CALLCODE, and DELEGATECALL, there can be two possibilites:
    #
    # 1) Once we find CALL, ..., we assume the contract can send Ether and thus has no problem
    # In this case we stop the search immediately
    elif MyGlobals.ETHER_LOCK_GOOD_IF_CAN_CALL and op in ['CALL','CALLCODE','DELEGATECALL']:
        global stop_search
        MyGlobals.stop_search = True
        return True, True 
    # 2) Once we find CALL, we still need to reach some STOP, RETURN, etc. 
    # In this case, we are more precise, but may lead to false positives
    else:   
        return True, False


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

    execute_one_block(ops,stack,0, trace, storage, mmemory, data, configurations,  ['CALL','CALLCODE','DELEGATECALL','SUICIDE'], ether_lock_can_send, 0, 0, debug, read_from_blockchain )




def check_one_contract_on_ether_lock(contract_bytecode, contract_address, debug = False, read_from_blockchain = False):


    print('\033[94m[ ] Check if contract is GREEDY\033[0m\n')
    print('[ ] Contract address   : %s' % contract_address)
    print('[ ] Contract bytecode  : %s...' % contract_bytecode[:50])
    print('[ ] Bytecode length    : %d' % len(contract_bytecode) )
    print('[ ] Debug              : %s' % debug)


    global MAX_CALL_DEPTH, symbolic_vars, symbolic_sha

    ops = parse_code( contract_bytecode, debug )

    #
    #
    # First check if Ether can be received by the contract
    #
    #

    MyGlobals.symbolic_vars = []
    initialize_params(read_from_blockchain, contract_address )
    set_params( 'call_value', '','100'  )
    clear_globals()

    MyGlobals.MAX_CALL_DEPTH = 1                    # Only one function has to be called 

    storage = {}    
    stack   = []
    mmemory = {}
    data = {}
    trace   = []
    configurations = {}
    execute_one_block(ops,stack,0, trace, storage, mmemory, data, configurations,  ['STOP','RETURN'], ether_lock_can_recieve, 0, 0, debug, read_from_blockchain )

    print(('\033[91m[-]' if not MyGlobals.stop_search else '\033[92m[+]')+'\033[0m \033[1mContract can receive Ether\033[0m' )

    # If it did not find, then the contract cannot receive Ether and thus it cannot lock ether (is not bad )
    if not MyGlobals.stop_search: 
        print('\n\033[92m[-] No lock vulnerability found because the contract cannot receive Ether \033[0m')
        return False


    #
    #
    # Then check if Ether can be released by the contract
    #
    #


    # If it does not have instructions that send Ether, then obviously it locks 
    if not code_has_instruction( ops, ['CALL','CALLCODE','DELEGATECALL','SUICIDE']) :
        #if debug: 
        print('\033[91m[-] The code does not have CALL/SUICIDE/DELEGATECALL/CALLCODE thus is greedy !\033[0m')
        return True
    if debug: print_code( contract_bytecode, ops )


    # Make some blockchain variables symbolic so they can take any value
    MyGlobals.symbolic_vars = ['CALLVALUE','CALLER','NUMBER','TIMESTAMP','BLOCKHASH','BALANCE','ADDRESS','ORIGIN','EXTCODESIZE']
    MyGlobals.symbolic_sha = True
    MyGlobals.symbolic_load= True

    
    #
    # Search
    #
    for i in range( 1 , MyGlobals.max_calldepth_in_normal_search + 1 ):

        run_one_check( i, ops, contract_address, debug, read_from_blockchain )
        if MyGlobals.stop_search: 
            print('\n\033[92m[+] No locking vulnerability found \033[0m')
            return False


    print('\n\n\033[91m[-] Locking vulnerability found! \033[0m' )
    return True

        




