from web3 import Web3
import json
import os

def run_deploy():
    # 连接到以太坊节点 (这里以本地节点为例)
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

    # 读取ABI和字节码
    b_dir = os.path.dirname(os.path.abspath(__file__))
    c_path = os.path.join(b_dir, 'DIDRegistry_abi.json')
    with open(c_path, 'r') as abi_file:
        abi = json.load(abi_file)

    b_dir = os.path.dirname(os.path.abspath(__file__))
    c_path = os.path.join(b_dir, 'DIDRegistry_bytecode.txt')
    with open(c_path, 'r') as bytecode_file:
        bytecode = bytecode_file.read()

    # 取出第一个可用的地址和私钥
    account = w3.eth.accounts[0]

    # 部署合约
    DIDRegistry = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = DIDRegistry.constructor().transact({'from': account})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return w3, abi, bytecode, account, tx_receipt.contractAddress

