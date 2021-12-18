# Maian 

The repository contains the Python implementation of Maian -- a tool for automatic detection of buggy Ethereum smart contracts of three different types: prodigal, suicidal and greedy. Maian processes contract's bytecode and tries to build a trace of transactions to find and confirm bugs. The technical aspects of the approach are described in the paper [I. Nikolic et al.: Finding the Greedy, Prodigal, and Suicidal Contracts at Scale, arXiv, 2018](https://arxiv.org/abs/1802.06038).

Maian was originally published in the repository https://github.com/ivicanikolicsg/MAIAN, but seems unmaintained since 2018.
This fork updates the code to recent (2021) versions of Python, geth, Z3, and web3. The graphical user interface has not yet been updated and probably will not yet work.

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



### GUI

For GUI inclined audience, we provide  a simple GUI-based Maian. Use `python gui-maian.py` to start it. 
A snapshot of one run is given below

![](./gui-maian.png)

## Installation

Maian should run smoothly on Linux (we've checked on Ubuntu) and MacOS. 
The list of dependencies is as follows:

1. `geth`, Go Ethereum, see https://geth.ethereum.org/docs/install-and-build
2. `python3`, Python3, see https://www.python.org/downloads
3. `z3`, Z3 constraint solver, see https://github.com/Z3Prover/z3
4. `solc`, Solidity compiler, check http://solidity.readthedocs.io/en/develop/installing-solidity.html
   Note that the correct version of the Solidity compiler depends on the version required by the source code you want to analyze.
   Check the information following `pragma solidity` in the `sol` files. Binaries of all versions can be found at https://github.com/ethereum/solidity/releases or https://github.com/ethereum/solc-bin
5. `web3.py`, the Python interface to Ethereum blockchains
6. PyQt5 (only for GUI Maian), try `sudo apt install python-pyqt5`

After installing `geth`, `python3` and `z3`, the following steps under Linux/MacOS should install MAIAN.

```console
$ git clone https://github.com/smartbugs/MAIAN.git # get MAIAN
$ cd MAIAN
$ python3 -m venv venv # we recomment to use a virtual environment
$ source venv/bin/activate # activate it before modifying or running MAIAN
$ pip install --upgrade pip # update Python's installer
$ pip install wheel
$ pip install web3 z3-solver
```
In case of problems, see `requirements.txt` for the package versions that work for us.

To run the sample contracts in the distribution,  we install the compiler for Solidity v0.4.x from the github repo `ethereum/solc-bin`
```console
$ wget https://github.com/ethereum/solc-bin/raw/gh-pages/linux-amd64/solc-linux-amd64-v0.4.26%2Bcommit.4563c3f
$ chmod +x solc-linux-amd64-v0.4.26+commit.4563c3fc
$ ln -s ../../solc-linux-amd64-v0.4.26+commit.4563c3fc venv/bin/solc
```
The last command installs the binary as `solc` whenever you activate the virtual environment.

Test the installation by running the sample contracts.
```console
$ cd tool
$ python maian.py -s example_contracts/ParityWalletLibrary.sol WalletLibrary -c 0
```

From now on, you need the following steps to run Maian.
```console
$ cd MAIAN/tool # go to the home directory of Maian
$ source ../venv/bin/activate # activate the virtual environment
$ python maian.py ... # run Maian
```

## Important

To reduce the number of false positives, Maian deploys the analyzed contracts (given either as Solidity or bytecode source) on 
a private blockchain, and confirms the found bugs by sending appropriate transactions to the contracts. 
Therefore, during the execution of the tool, a private Ethereum blockchain is running in the background (blocks are mined on it in the same way as on the Mainnet). Our code stops the private blockchain once Maian finishes the search, however, in some  extreme cases, the blockchain keeps running. Please make sure that after the execution of the program, the private blockchain is off (i.e. `top` does not have `geth` task that corresponds to the private blockchain). 

## License

Maian is released under the [MIT License](https://opensource.org/licenses/MIT), i.e. free to use it for private and commercial purposes.

 
