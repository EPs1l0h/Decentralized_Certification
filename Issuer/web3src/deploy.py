from web3 import Web3
import json
import os

from account import read_ganache_accounts

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
accounts = read_ganache_accounts()

# 取出第一个可用的地址和私钥
addr, private_key = accounts.pop(0)
account = addr

# 更新ganache_output.txt，移除已分配的账号
with open('ganache_output.txt', 'w') as file:
    file.write('Ganache CLI v6.12.2 (ganache-core: 2.13.2)\n\n')
    file.write('Available Accounts\n==================\n')
    for i, (addr, private_key) in enumerate(accounts):
        file.write(f'({i}) {addr} (100 ETH)\n')
    file.write('\nPrivate Keys\n==================\n')
    for i, (addr, private_key) in enumerate(accounts):
        file.write(f'({i}) {private_key}\n')

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
