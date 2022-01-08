# Maian 

This repository contains the Python implementation of Maian -- a tool for automatic detection of buggy Ethereum smart contracts of three different types: prodigal, suicidal and greedy. Maian processes the bytecode of contracts and searches for sequences of transactions that trigger a bug. The technical aspects of the approach are described in the paper [I. Nikolic et al.: Finding the Greedy, Prodigal, and Suicidal Contracts at Scale, arXiv, 2018](https://arxiv.org/abs/1802.06038).

Maian was originally published in the repository https://github.com/ivicanikolicsg/MAIAN, but seems unmaintained since 2018.
This fork updates the code (except for the graphical interface) to recent (Dec 2021) versions of Python, geth, Z3, and web3.

## Evaluating Contracts
Maian analyzes smart contracts defined in a file `<contract file>` with:  

1. Solidity source code, use `-s <contract file> <main contract name>`
2. Bytecode source, use `-bs <contract file>`
3. Bytecode compiled (i.e. the code sitting on the blockchain), use `-b <contract file>`

Maian checks for three types of buggy contracts:

1. Suicidal contracts (can be killed by anyone, like the Parity Wallet Library contract), use `-c 0`
2. Prodigal contracts (can send Ether to anyone), use `-c 1`
3. Greedy contracts (nobody can get out Ether), use `-c 2`

For instance, to check if the contract `ParityWalletLibrary.sol` given in Solidity source code with `WalletLibrary` as main contract is suicidal use

	$ python maian.py -s example_contracts/ParityWalletLibrary.sol WalletLibrary -c 0

The output should look like this:

![smiley](maian.png)

To get the full list of options use `python maian.py -h`


## Installation

Maian should run smoothly on Linux (we've checked Ubuntu 18.04.6 and 20.04.3) and MacOS. 
The list of dependencies is as follows:

1. `geth`, Go Ethereum, see https://geth.ethereum.org/docs/install-and-build
2. `python3`, Python3, see https://www.python.org/downloads
3. `z3`, Z3 constraint solver, see https://github.com/Z3Prover/z3
4. `solc`, Solidity compiler, check http://solidity.readthedocs.io/en/develop/installing-solidity.html

   Note that the correct version of the Solidity compiler depends on the source code you want to analyze.
   Check the information following `pragma solidity` in the `sol` files. Binaries of all versions can be found at https://github.com/ethereum/solidity/releases or https://github.com/ethereum/solc-bin
5. `web3.py`, the Python interface to Ethereum blockchains

After installing `geth`, `python3` and `z3`, **the following steps install Maian under Linux/MacOS**.

```console
git clone https://github.com/smartbugs/MAIAN.git # download Maian
cd MAIAN
python3 -m venv venv # we suggest to use a virtual environment # or python3.8 -m ... for Python 3.8 
source venv/bin/activate # activate it before using Maian
pip install --upgrade pip # update Python's installer
pip install wheel
pip install web3 z3-solver
```
See `requirements-3.6.txt` and `requirements-3.8.txt` for the package versions that work for us (in conjunction with Python 3.6.9 or 3.8.10, Z3 4.8.14 and Geth 1.10.14-stable).

**To analyze the sample contracts in the distribution,**  we install the compiler for Solidity v0.4.x from the github repo `ethereum/solc-bin`.
```console
wget https://github.com/ethereum/solc-bin/raw/gh-pages/linux-amd64/solc-linux-amd64-v0.4.26%2Bcommit.4563c3fc
chmod +x solc-linux-amd64-v0.4.26+commit.4563c3fc
ln -s ../../solc-linux-amd64-v0.4.26+commit.4563c3fc venv/bin/solc
```
The last command makes the binary available as `solc` if the virtual environment is activated.

Test the installation by analyzing the sample contracts.
```console
cd tool
python maian.py -s example_contracts/ParityWalletLibrary.sol WalletLibrary -c 0
python maian.py -s example_contracts/ParityWalletLibrary.sol WalletLibrary -c 1
python maian.py -s example_contracts/ParityWalletLibrary.sol WalletLibrary -c 2
python maian.py -b example_contracts/example_greedy.bytecode -c 2 # runtime/deployed bytecode
python maian.py -bs example_contracts/example_lock.bytecode_source -c 0 # creation/deployment bytecode
```

**Once installed, run Maian subsequently as follows.**
```console
cd MAIAN/tool # go to the home directory of Maian
source ../venv/bin/activate # activate the virtual environment
python maian.py ... # run Maian
```

## Important

To reduce the number of false positives, Maian deploys the analyzed contracts (given either as Solidity or bytecode source) on 
a private blockchain, and confirms the found bugs by sending appropriate transactions to the contracts. 
Therefore, during the execution of the tool, a private Ethereum blockchain is running in the background (blocks are mined on it in the same way as on the Mainnet). Our code stops the private blockchain once Maian finishes the search, however, in some  extreme cases, the blockchain keeps running. Please make sure that after the execution of the program, the private blockchain is off (i.e. `top` does not have `geth` task that corresponds to the private blockchain). 

## License

Maian is released under the [MIT License](https://opensource.org/licenses/MIT), i.e. free for private and commercial use.

 
