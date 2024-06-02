import hashlib
import sqlite3
import uuid

from flask import Flask, request, jsonify

from web3src.account import read_ganache_accounts

app = Flask(__name__)

# 和持有者交互 - 注册
@app.route('/register', methods=['POST'])
def register():
    # data = request.get_json()
    # 处理注册逻辑
    # 这里和数据库交互，从ganache_output.txt里面拿addr和私钥（上链用的是interact_with_contract.py里面的函数）
    data = request.json
    account = data.get('account')
    password = data.get('password')

    # 生成DID
    did = str(uuid.uuid4())

    # 从文件中读取地址和私钥
    accounts = read_ganache_accounts()

    # 检查是否有可用的地址和私钥
    if not accounts:
        return jsonify({'message': 'No available accounts in ganache_output.txt'}), 500

    # 取出第一个可用的地址和私钥
    addr, private_key = accounts.pop(0)

    # 存储数据到数据库
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    cursor.execute('''
            INSERT INTO Holder (account, password, addr, private_key, did)
            VALUES (?, ?, ?, ?, ?)
        ''', (account, hashlib.sha256(password.encode()).hexdigest(), addr, private_key, did))
    conn.commit()
    conn.close()

    # 更新ganache_output.txt，移除已分配的账号
    with open('ganache_output.txt', 'w') as file:
        file.write('Ganache CLI v6.12.2 (ganache-core: 2.13.2)\n\n')
        file.write('Available Accounts\n==================\n')
        for i, (addr, private_key) in enumerate(accounts):
            file.write(f'({i}) {addr} (100 ETH)\n')
        file.write('\nPrivate Keys\n==================\n')
        for i, (addr, private_key) in enumerate(accounts):
            file.write(f'({i}) {private_key}\n')

    # 返回
    return jsonify({"message": "Registration Successful"}), 200

# 和持有者交互 - 登录
@app.route('/login', methods=['POST'])
def login():
    # data = request.get_json()
    # 处理登录逻辑
    # 这里和数据库交互，从ganache_output.txt里面拿addr和私钥（上链用的是interact_with_contract.py里面的函数）
    # 返回
    data = request.json
    account = data.get('account')
    password = data.get('password')

    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    cursor.execute('''
           SELECT private_key, addr, did FROM Holder WHERE account = ? AND password = ?
       ''', (account, hashlib.sha256(password.encode()).hexdigest()))
    result = cursor.fetchone()
    conn.close()

    if result:
        private_key, addr, did = result
        return jsonify({'private_key': private_key, 'addr': addr, 'did': did}),200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# 和颁发者交互
@app.route('/verifyDID', methods=['POST'])
def verifyDID():
    data = request.get_json()  # 这里的data是一整个DID document的json
    import os
    import sys

    current_dir = os.getcwd()  # 保存当前工作目录
    src_dir = os.path.join(current_dir, 'web3src')  # 构造web3src的绝对路径

    try:
        sys.path.insert(0, src_dir)  # 将web3src添加到sys.path
        from web3src.verify_did import verify_did  # 导入verify_did模块
    finally:
        sys.path.pop(0)  # 无论如何，最后都恢复sys.path

    # 调用verify_did函数
    b_dir = os.path.dirname(os.path.abspath(__file__))
    c_path = os.path.join(b_dir, 'web3src/contract_address.txt')
    with open(c_path, 'r') as file:
        contract_address = file.read()
    lld = verify_did(contract_address, data)
    return lld

# 和验证者交互 - 验证VC
@app.route('/verifyVC', methods=['POST'])
def verifyVC():
    # 获取请求数据
    data = request.get_json()
    from web3src.verify_vc import verify_vc
    lld = verify_vc(data['vc'])  # 这里是不是得根据需要改一下？
    # 处理VC验证逻辑
    # ...
    return lld

# 和验证者交互 - 验证VP
@app.route('/verifyVP', methods=['POST'])
def verifyVP():
    # 获取请求数据
    data = request.get_json()
    from web3src.verify_vp import verify_vp
    lld = verify_vp(data['vp'])  # 这里是不是得根据需要改一下？
    # 处理VP验证逻辑
    # ...
    return lld

if __name__ == '__main__':
    app.run(debug=True)
