from runweb3 import Web3
import json
import os
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

# 使用提供的地址进行交易
account = '0x4e0b15cAF28fD201A6ff5C17B3ff8227095462aA'

# 部署合约
DIDRegistry = w3.eth.contract(abi=abi, bytecode=bytecode)

def deploy_contract():
    """部署合约并返回合约地址"""
    tx_hash = DIDRegistry.constructor().transact({'from': account})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt.contractAddress

if __name__ == "__main__":
    contract_address = deploy_contract()
    print(f"Contract deployed at: {contract_address}")
    # 将合约地址写入文件
    b_dir = os.path.dirname(os.path.abspath(__file__))
    c_path = os.path.join(b_dir, 'contract_address.txt')    
    with open(c_path, 'w') as f:
        f.write(contract_address)
