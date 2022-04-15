from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# Compile Solidity file

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

# print(compiled_sol)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
# print("compiled_sol :", compiled_sol)
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi -> like interface where we see all names of attributes/methods we can call on contract
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]
# The Contract Application Binary Interface (ABI) is the standard way to interact with contracts in the Ethereum ecosystem, both from outside the blockchain and for contract-to-contract interaction.
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/8d4f20496b22482592f9291b9526c6a2")
)
# chain_id = w3.eth.chain_id
chain_id = 4

my_address = "0x2374bB026d9af730F3EB8fCb76482e93F0e21040"

# priv_key = "0x9305778b8fa19de776ba60ec998713e7171534a191cdf27829b6250426b5a687"
# for priv key , we place a "0x" at the start, always
# NEVER post your wallet private key, use environment variables
priv_key = os.getenv("SOL_PRIVATE_KEY")  # uses local .env

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# print(SimpleStorage)  # <class 'web3._utils.datatypes.Contract'>

# nonce = something used just once
# get the latest transaction:
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)


# 1. Build Transaction
# 2. Sign a T
# 3. Send a T

transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)
# signed transaction -> need to use the priv key to generate the message signature #2
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=priv_key)

# send this signed transaction
print(" Deploying contract ... ")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(" Deployed!! ")
# Working with the contract, you will need:
# 1. Contract ABI
# 2. Contract address

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# call -> simulate making the call and getting the return value
# transact -> actually make a state change -> modify the blockchain?

retrieve_return = (
    simple_storage.functions.retrieve().call()
)  # call, wont make a state change with .call
print("retrieve_return :", retrieve_return)


# store = simple_storage.functions.store(15).call()  # call is just a simulation
# print("store :", store) # not actually modifying the blockchain

# Initial value of favorite numer
print(" Updating contract with store of 15... ")

store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)
# we use nonce + 1 because we used the original nonce to create our initial transaction call constructor -> line 70

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=priv_key
)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print(" Updated! ")
retrieve_return2 = (
    simple_storage.functions.retrieve().call()
)  # since we sent a tx to blockchain, it now should retrieve a favNumber
print(
    "retrieve_return2 :", retrieve_return2
)  # returns 15 because we called store(15) before

# ganache-cli docs : https://www.npmjs.com/package/ganache-cli
# https://github.com/trufflesuite/ganache/releases/tag/v7.0.0
