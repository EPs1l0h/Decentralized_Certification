from web3 import Web3
import json

# 连接到以太坊节点 (这里以本地节点为例)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# 读取ABI和字节码
with open('DIDRegistry_abi.json', 'r') as abi_file:
    abi = json.load(abi_file)

with open('DIDRegistry_bytecode.txt', 'r') as bytecode_file:
    bytecode = bytecode_file.read()

# 使用提供的地址进行交易
account = '0x23F884761b3779a6fa8016660772f3aA638908AF'

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
    with open('contract_address.txt', 'w') as f:
        f.write(contract_address)
