from instruction_list import *

def print_code(code,ops):
    for o in ops:
        print('%6x  : %4d : %2s : %12s : %s' % (o['id'],o['id'], o['op'],o['o'] , o['input']) )
    print('Total byte/code size: %d %d' % (len(code)/2,len(ops)) )

def get_one_op( code, pos, size_of_input, debug=False ):
    if pos + 2 + size_of_input > len(code ):
        if debug: print('Incorrect code op at %x : %d : %d :  %s' % (pos/2, pos+2+size_of_input, len(code), code[pos:] ) )
    instruction = '0x' + code[pos:pos+2]
    o = ''
    if instruction in cops:
        o = cops[ instruction ]
    t = {'id':int(pos/2),'op':code[pos:pos+2],'input':code[pos+2:pos+2+2*size_of_input],'o':o}
    return (pos + 2 + 2*size_of_input, t)

def parse_code( code, debug = False):
    ops = list()

    i = 0;
    while i < len(code):

        op = code[i:i+2]

        if op >= '60' and op <='7f':
            i, t = get_one_op( code, i, int(op,16) - int('60',16)+1, debug )
            ops.append(t)
        else:
            i, t = get_one_op( code, i, 0, debug );
            ops.append(t)

    return ops

def code_has_instruction( code, ops):

    for o in code: 
        if o['o'] in ops:
            return True

    return False


def get_dictionary_of_ops( ops ):
    d = {}
    for t in ops:
        if t['op'] not in d: d[ t['op'] ] = True
    return d

def has_call( ops ):
    for t in ops:
        if t['op'] == 'f1': return True
    return False

def find_pos( code, byte_position):
    found = -1
    for i in range(len(code)) :
        if code[i]['id'] == byte_position:
            found = i
    if found >= 0 and code[found]['o'] == 'JUMPDEST':
        return found

    return -1

