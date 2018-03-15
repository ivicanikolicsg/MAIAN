from __future__ import print_function
from values import MyGlobals
from hashlib import *
from z3 import *


def print_stack(stack):
    print('\033[90m------------------------------------- STACK -------------------------------------')
    for s in stack[::-1]:
        if 'z3' in s:
            if is_bv_value( simplify(s['z3'])): print('%10s : %4x  : %x' % (s['type'],s['step'],simplify(s['z3']).as_long() ) )
            else: print('%10s : %4x  : %s' % (s['type'],s['step'], simplify(s['z3']) ) )
        else:
            print('%10s : %4x  ' % (s['type'],s['step']) )
    print('\033[0m')

def print_storage(storage):
    print('************************************ STORAGE ************************************')
    for fl in storage:
        for s in storage[fl]:
            print('\033[91m[ %64x ] \033[0m : ' % (fl), end='' )        
            if is_bv_value( simplify(s['z3'])): print('%x' % (simplify(s['z3']).as_long() ) )
            else: print('%s' % (simplify(s['z3']) ) )

def print_memory(mmemory):
    print('************************************ MEMORY ************************************')
    for m in mmemory:
        fl = mmemory[m]
        print('\033[91m[ %64x ] \033[0m : ' % (m), end='' )        
        if fl['type'] == 'undefined' : print('undefined' )
        elif is_bv_value( simplify(fl['z3'])): print('%x' % (simplify(fl['z3']).as_long() ) )
        else: print('%s' % (simplify(fl['z3']) ) )            
        

def print_trace(trace):
    print('++++++++++++++++++++++++++++ Trace ++++++++++++++++++++++++++++')
    for o in trace:
        print('%6x  : %2s : %12s : %s' % (o['id'],o['op'],o['o'] , o['input']) )


# Computes hash of input
def get_hash(txt):
    k = md5()
    k.update(txt.encode('utf-8'))
    return int(k.hexdigest(),16)

# Determines the TX inputs so that the contract can be exploited
def get_function_calls( calldepth, debug ):

    global s, no_function_calls, function_calls


    if MyGlobals.s.check() == sat:


        m = MyGlobals.s.model()

        if debug: print('\nSolution:')
        sol = {}
        for d in m:
            if debug: print('%s -> %x' % (d,m[d].as_long() ) )
            sol[str(d)] = '%x' % m[d].as_long()


        function_inputs = {}
    
        # Get separate calldepth inputs
        for cd in range (1,calldepth+1):

            
            # Find next free
            next_free = 0
            for f in range(100):
                if ('input'+str(cd)+'['+str(4+32*f)+']') in sol or ('input'+str(cd)+'['+str(4+32*f)+']d') in sol:
                    next_free = 32*f + 32

            # Fix weird addresses
            for f in range(100):
                addr = 'input'+str(cd)+'['+str(4+32*f)+']d'
                if addr in sol:
                    old_address = int(sol[addr],16)  
                    del sol[addr]
                    sol[addr[:-1]] =  '%x'% next_free

                    for offset in range(100):
                        check_address = 'input'+str(cd)+'['+('%x'%(4+old_address + 32*offset))+']'
                        if check_address in sol:
                            sol['input'+str(cd)+'['+'%d'%(4+int(next_free)) +']' ] = sol[check_address]
                            del sol[check_address]
                            next_free += 32


            # Produce the input of the call
            tmp_one = {}
            for addr in sol:
                if addr.find('input'+str(cd)+'[') >= 0:
                    tmp_one[addr] = sol[addr]




            # The function hash
            function_hash = 'input'+str(cd)+'[0]'
            if function_hash not in tmp_one:
#               print('Cannot find function hash')
#               print(tmp_one)
                return False

            
            if len(tmp_one[ function_hash] [:-56]) > 0:
                function_inputs[cd] = '%08x'% int(tmp_one[ function_hash] [:-56],16)
            else:
                function_inputs[cd] = '0'
    
            del tmp_one[function_hash]
            


            # Function arguments
            max_seen = 4
            for offset in range(100):
                addr = 'input'+str(cd)+'['+'%d'%(4+offset*32)+']'
                if addr in tmp_one:
                    function_inputs[cd] = function_inputs[cd] + '%064x' % int(tmp_one[addr],16)
                    max_seen = 4+(offset+1)*32
                    del tmp_one[addr]
                else:
                    function_inputs[cd] = function_inputs[cd] + '%064x' % 0

            function_inputs[cd] = function_inputs[cd][:2*max_seen]

            if len(tmp_one) > 0:
                print('Some addresses are larger')
                print(tmp_one)
                return False




        MyGlobals.no_function_calls = calldepth
        MyGlobals.function_calls = {}
        for n in range(10):
            if n in function_inputs:
                call_value = 0
                for d in m: 
                    if str(d) == ('CALLVALUE-'+str(n)):
                        call_value = m[d].as_long()
                MyGlobals.function_calls[n] = {'input':function_inputs[n],'value': call_value}
        

        if calldepth != len(MyGlobals.function_calls):
            MyGlobals.no_function_calls = 0
            MyGlobals.function_calls = {}

            return False

        #print(MyGlobals.function_calls)
        if debug:
            for n in range(calldepth):
                print('- %d - %10x -  ' % (n+1, MyGlobals.function_calls[n+1]['value'] ), end='' )
                for j in range(len(MyGlobals.function_calls[n+1]['input'] )):
                    if (j-8) % 64 == 0: print(' ',end='')
                    print('%s' % MyGlobals.function_calls[n+1]['input'][j], end='')
                print('') 

        return True


    else:

        MyGlobals.no_function_calls = 0
        return False


