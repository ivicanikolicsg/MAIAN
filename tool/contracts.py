from web3 import Web3
import os.path
import json
import sys
import glob
import sys
import json
import rlp
from subprocess import Popen, PIPE, STDOUT
from values import MyGlobals
from blockchain import *

def compile_contract(filename):

    print('\033[1m[ ] Compiling Solidity contract from the file %s ... \033[0m' % filename, end='')

    source_file = filename
    if (not os.path.isfile(source_file) ):
        print('\n\033[91m[-] Contract file %s does NOT exist\033[0m' % source_file )
        return

    with open(filename, 'r') as myfile:
        code=myfile.read()
    
    p=Popen(['solc','--bin','--abi','-o','out',source_file,'--overwrite'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    solo = ''
    while p.poll() is None:
        l = p.stdout.readline()
        solo += bytes.decode(l)
    if 'Error' in solo:
        print(solo)
        print('\n\033[91m[-] Cannot compile the contract \033[0m')
        exit()
    p.wait()

    print('\033[92m Done \033[0m')


def get_function_hashes(contract):

        
    data = json.load(open('out/'+contract+'.abi'))
    fhashes = {}
    for d in data:
        if 'type' in d and d['type'] == 'function':
            hs = ''
            if 'name' in d: hs = d['name']
            fr = True
            hs += '('
            if 'inputs' in d:
                for i in d['inputs']:
                    if not fr: hs +=','
                    hs += i['type']
                    fr = False
            hs += ')'
            hash_op = Web3.keccak(text=hs).hex()

            fhashes[hash_op[2:10]] = hs

    return fhashes



def deploy_contract(filename, etherbase, rawcode = False):

    if rawcode:
        with open(filename, 'r') as myfile: byt=myfile.read()
        filename_write_address = os.path.basename(filename)+'.address'
        
    else:
        filename_abi = os.path.basename(filename)+'.abi'
        filename_bin = os.path.basename(filename)+'.bin'
        filename_write_address = os.path.basename(filename)+'.address'
        with open('./out/'+filename_abi, 'r') as myfile: abi=myfile.read()
        with open('./out/'+filename_bin, 'r') as myfile: byt=myfile.read()
        if( len(abi) == 0 or len(byt) == 0 ):
            print('\033[91m[-] Some of the files is missing or empty: |%s|=%d  |%s|=%d' % (filename_abi, len(abi), filename_bin, len(byt) ) )
            print('The contracts have NOT been deployed\033[0m')
            return

        abi = json.loads(abi)

    print('\033[1m[ ] Deploying contract \033[0m', end='')
    MyGlobals.web3.geth.personal.unlock_account(etherbase, '1', 15000)


    try:
        tx = {'from':etherbase, 'data': ('0x' if byt[0:2]!='0x' else '') +byt , 'gas':6000000}
        transaction_creation_hash = MyGlobals.web3.eth.sendTransaction( tx ).hex()
        receipt = MyGlobals.web3.eth.wait_for_transaction_receipt(transaction_creation_hash,timeout=120,poll_latency=0.1)
        contract_address = receipt['contractAddress']
    except Exception as e:
        print ("Exception: "+str(e))
        return None

    print('\033[92m confirmed at address: %s \033[0m' % contract_address)
    fullcode = MyGlobals.web3.eth.getCode(contract_address)
    print('\033[1m[ ] Contract code length on the blockchain : \033[0m \033[92m  %d  : %s... \033[0m' % (len(fullcode), fullcode.hex()[:30] ) )
    with open('./out/'+filename_write_address, 'w') as f:
        f.write(contract_address)
        f.close()
    print('\033[1m[ ] Contract address saved in file: \033[0m\033[92m%s \033[0m' % ('./out/'+filename_write_address))

    return contract_address

def rlp_encode(input):
    if isinstance(input,str):
        if len(input) == 1 and ord(input) < 0x80: return input
        else: return encode_length(len(input), 0x80) + input
    elif isinstance(input,list):
        output = ''
        for item in input: output += rlp_encode(item)
        return encode_length(len(output), 0xc0) + output

def encode_length(L,offset):
    if L < 56:
         return chr(L + offset)
    elif L < 256**8:
         BL = to_binary(L)
         return chr(len(BL) + offset + 55) + BL
    else:
         raise Exception("input too long")

def to_binary(x):
    if x == 0:
        return ''
    else: 
        return to_binary(int(x / 256)) + chr(x % 256)    

def normalize_address(x, allow_blank=False):
    if allow_blank and x == '':
        return ''
    if len(x) in (42, 50) and x[:2] == '0x':
        x = x[2:]
    if len(x) in (40, 48):
        x = bytes.fromhex(x)
    if len(x) == 24:
        assert len(x) == 24 and Web3.keccak(x[:20])[:4] == x[-4:]
        x = x[:20]
    if len(x) != 20:
        raise Exception("Invalid address format: %r" % x)
    return x
     

def predict_contract_address(accountAddress):

    nonce = int(MyGlobals.web3.eth.getTransactionCount(accountAddress)) 
    adr = Web3.keccak(rlp.encode([normalize_address(accountAddress), nonce]))[-20:]
    return Web3.toChecksumAddress(adr.hex())



