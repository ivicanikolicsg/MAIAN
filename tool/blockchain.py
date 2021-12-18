import subprocess, signal
import time
import sys
import os
from values import MyGlobals

from web3 import Web3
MyGlobals.web3 = Web3(Web3.HTTPProvider(f"http://127.0.0.1:{MyGlobals.port_number}"))




def start_private_chain(chain,etherbase,debug=False):

    devnull = open(os.devnull, 'w')


    if chain!= 'remptychain':

        # Remove previous blockchain
        pr=subprocess.run(['rm','-rf','./blockchains/'+chain])

        # Init new blockchain
        cmd = ['geth','--datadir','./blockchains/'+chain,'init','./blockchains/genesis.json']
        if debug: pr=subprocess.run(cmd)
        else: pr=subprocess.run(cmd,stdout=devnull, stderr=devnull)

        # Copy the accounts
        pr=subprocess.run(['cp','-r','./blockchains/remptychain/keystore','./blockchains/'+chain+'/'])



    if MyGlobals.web3.isConnected() :
            print('\033[91m[-] Some blockchain is active, killing it... \033[0m', end='')
            kill_active_blockchain()
            if not MyGlobals.web3.isConnected():
                print('\033[92m Killed \033[0m')
            else:
                print('Cannot kill')
    
    print('\033[1m[ ] Connecting to PRIVATE blockchain %s  \033[0m' % chain, end='')
    cmd = ['geth','--http','--http.api=eth,net,web3,personal', '--http.port',MyGlobals.port_number,
            '--datadir','blockchains/'+chain,'--networkid','123','--mine','--miner.threads=1',
            '--port',MyGlobals.port_network,
            '--allow-insecure-unlock', '--snapshot=false', '--maxpeers=0',
            '--dev',
            '--miner.etherbase', MyGlobals.etherbase_account,
            '--unlock', MyGlobals.etherbase_account,
            '--password', './blockchains/password.txt'
          ]
    if debug:
        pro = subprocess.Popen(cmd)
    else:
        pro = subprocess.Popen(cmd,stdout=devnull, stderr=devnull)

    while not MyGlobals.web3.isConnected():
        print('',end='.')
        if MyGlobals.exec_as_script:
            sys.stdout.flush()        
        time.sleep(1)

    if MyGlobals.web3.isConnected():
        print('\033[92m ESTABLISHED \033[0m')
    else:
        print('\033[93m[-] Connection failed. Exiting\033[0m')
        exit(2)
    
    return pro


def kill_active_blockchain():

    devnull = open(os.devnull, 'w')    
    p = subprocess.Popen(['fuser',MyGlobals.port_number+'/tcp'], stdout=subprocess.PIPE, stderr=devnull)
    out, err = p.communicate()
    for line in out.splitlines():
        pid = int(line.split(None, 1)[0])
        os.kill(pid, signal.SIGKILL)
        time.sleep(0.5)

    devnull = open(os.devnull, 'w')    
    #p = subprocess.Popen(['lsof','+D','blockchains/','-t' ], stdout=subprocess.PIPE, stderr=devnull)
    p = subprocess.Popen(['lsof','-t','-i','tcp:'+MyGlobals.port_number ], stdout=subprocess.PIPE, stderr=devnull)
    out, err = p.communicate()
    for line in out.splitlines():
        pid = int(line.split(None, 1)[0])
        p2 = subprocess.Popen(['ps','-p',str(pid) ], stdout=subprocess.PIPE, stderr=devnull)
        out2,err2 = p2.communicate()
        if bytes.decode(out2).find('datadir') >= 0:
            os.kill(pid, signal.SIGKILL)
        time.sleep(1)


def execute_transactions(txs):


    count = 0
    weiused = 0
    for tx in txs:
        MyGlobals.web3.geth.personal.unlock_account(tx['from'],'1',15000)
        try:
            hash = MyGlobals.web3.eth.sendTransaction( tx )

            while MyGlobals.web3.eth.getTransaction(hash)['blockNumber'] is None:
                print('.',end='')
                if MyGlobals.exec_as_script:
                    sys.stdout.flush()
                time.sleep(1)
            print(' tx[%d] mined ' % count, end='')

            weiused += MyGlobals.web3.eth.getTransactionReceipt(hash)['gasUsed'] * MyGlobals.web3.eth.getTransaction(hash)['gasPrice']

        except Exception as e:
            print ("Exception: "+str(e))

        count +=1

    return weiused






