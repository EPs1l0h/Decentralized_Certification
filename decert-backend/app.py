import hashlib
import sqlite3
import json
import os
from datetime import datetime, timezone
from flask_cors import cross_origin
from web3 import Web3
from flask import Flask, request, jsonify
import requests

from web3src.generate_vc import generate_vc

import socket


app = Flask(__name__)

w3 = None
abi = None
bytecode = None
account_addr = ''
contract_addr = ''
user_name = ''
is_login = False
flask_ip_addr = '127.0.0.1'
flask_port = 5000


def deploy():
    global w3, account_addr
    # 部署合约
    DIDRegistry = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = DIDRegistry.constructor().transact({'from': account_addr})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    b_dir = os.path.dirname(os.path.abspath(__file__))
    contract_addr = tx_receipt.contractAddress
    c_path = os.path.join(b_dir, 'contract_address')
    with open(c_path, 'w') as bytecode_file:
        bytecode_file.write(contract_addr)
    return contract_addr


def check_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # 读取文件内容
            file_content = file.read()
            # 如果文件内容不为空则返回true，否则返回false
            if file_content:
                return file_content
            else:
                return False
    except FileNotFoundError:
        print(f"file {file_path} not found")
        return False


def init_func():
    global w3, abi, bytecode, account_addr, contract_addr
    # 连接到以太坊节点 (这里以本地节点为例)
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    # 读取ABI和字节码
    b_dir = os.path.dirname(os.path.abspath(__file__))
    c_path = os.path.join(b_dir, 'web3src/DIDRegistry_abi.json')
    with open(c_path, 'r') as abi_file:
        abi = json.load(abi_file)

    b_dir = os.path.dirname(os.path.abspath(__file__))
    c_path = os.path.join(b_dir, 'web3src/DIDRegistry_bytecode.txt')
    with open(c_path, 'r') as bytecode_file:
        bytecode = bytecode_file.read()

    # 取出第一个可用的地址
    account_addr = w3.eth.accounts[0]

    b_dir = os.path.dirname(os.path.abspath(__file__))
    c_path = os.path.join(b_dir, "contract_address")
    chk_file = check_file(c_path)
    if chk_file:
        contract_addr = chk_file
    else:
        contract_addr = deploy()

    from sqlite import init_sqlite
    init_sqlite()


@app.route('/checkUserName', methods=['POST'])
@cross_origin()
def checkUserName():
    """
    轮询，返回是否在线
    """
    print("========== 开始执行 checkUserName 函数 ==========")
    global is_login, user_name
    print(f"当前登录状态: is_login={is_login}, user_name={user_name}")

    if is_login:
        response_data = {'isValid': True, 'username': user_name}
        print("返回给前端的数据:")
        print(json.dumps(response_data, indent=4))
        print("========== checkUserName 函数执行完毕 ==========\n")
        return jsonify(response_data)
    else:
        response_data = {'isValid': False, 'username': ''}
        print("返回给前端的数据:")
        print(json.dumps(response_data, indent=4))
        print("========== checkUserName 函数执行完毕 ==========\n")
        return jsonify(response_data)


# 和持有者交互 - 注册
@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    """
    data = request.get_json()
    处理注册逻辑
    这里和数据库交互，从ganache_output.txt里面拿addr和私钥（上链用的是interact_with_contract.py里面的函数）
    """
    print("========== 开始执行 register 函数 ==========")
    data = request.json
    print("接收到前端的数据:")
    print(json.dumps(data, indent=4))

    global is_login, user_name
    user_name = data.get('username')
    is_login = True
    password = data.get('password')
    password_confirm = data.get('password_confirm')
    algorithm = data.get('algorithm')

    if password != password_confirm:
        response_data = {"message": "Registration Failed"}
        print("返回给前端的数据:")
        print(json.dumps(response_data, indent=4))
        print("========== register 函数执行完毕 ==========\n")
        return jsonify(response_data), 401
    global account_addr
    did_document = registerDID(algorithm)
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Holder(account, password, addr, did_document) 
        VALUES(?, ?, ?, ?)
    ''', (user_name, password, account_addr, did_document))
    conn.commit()
    conn.close()

    # 返回
    response_data = {"message": "Registration Successful"}
    print("返回给前端的数据:")
    print(json.dumps(response_data, indent=4))
    print("========== register 函数执行完毕 ==========\n")
    return jsonify(response_data), 200


# 获取Holder信息
@app.route('/get_holder_info', methods=['GET'])
@cross_origin()
def get_holder_info():
    """
    获取 username 和 did
    """
    print("========== 开始执行 get_holder_info 函数 ==========")
    global is_login
    if not is_login:
        response_data = {'isValid': False, 'username': 'None'}
        print("返回给前端的数据:")
        print(json.dumps(response_data, indent=4))
        print("========== get_holder_info 函数执行完毕 ==========\n")
        return jsonify(response_data)
    else:
        conn = sqlite3.connect('accounts.db')
        cursor = conn.cursor()
        cursor.execute('SELECT did_document FROM Holder')
        did_document_tuple = cursor.fetchone()
        did_document = did_document_tuple[0]
        did_document = json.loads(did_document)
        did = did_document['id']
        conn.close()

        response_data = {
            'isValid': True,
            'username': user_name,
            'DID': did
        }
        print("返回给前端的数据:")
        print(json.dumps(response_data, indent=4))
        print("========== get_holder_info 函数执行完毕 ==========\n")
        return jsonify(response_data)


# 和持有者交互 - 登录
@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    """
    data = request.get_json()
    处理登录逻辑
    这里和数据库交互，从ganache_output.txt里面拿addr和私钥（上链用的是interact_with_contract.py里面的函数）
    返回
    """
    print("========== 开始执行 login 函数 ==========")
    data = request.json
    print("接收到前端的数据:")
    print(json.dumps(data, indent=4))

    account = data.get('account')
    password = data.get('password')
    global is_login, user_name
    is_login = True
    user_name = account
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    cursor.execute('''
           SELECT addr, addr FROM Holder WHERE account = ? AND password = ?
       ''', (account, hashlib.sha256(password.encode()).hexdigest()))
    result = cursor.fetchone()
    conn.close()

    response_data = {'isValid': True}
    print("返回给前端的数据:")
    print(json.dumps(response_data, indent=4))
    print("========== login 函数执行完毕 ==========\n")
    return jsonify(response_data), 200


@app.route('/requestAuthenticateDID', methods=['POST'])
@cross_origin()
def requestAuthenticateDID():
    """
    持有者发给颁发者DID
    """
    print("========== 开始执行 requestAuthenticateDID 函数 ==========")
    global flask_ip_addr, flask_port
    Issuer_ip_addr = flask_ip_addr
    port = flask_port
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()

    cursor.execute("SELECT did_document FROM Holder WHERE id = 1")
    did = cursor.fetchone()
    data = json.loads(did[0])
    conn.close()
    url = f'http://{Issuer_ip_addr}:{port}/recDID'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=data)

    print("发送给颁发者的数据:")
    print(json.dumps(data, indent=4))
    print("颁发者响应:")
    print(response)
    return jsonify({"isValid":True})
    print("========== requestAuthenticateDID 函数执行完毕 ==========\n")


@app.route('/holderRequestVC', methods=['POST'])
@cross_origin()
def holderRequestVC():
    """
    持有者返回已有的VC给前端
    """
    print("========== 开始执行 holderRequestVC 函数 ==========")
    global is_login
    if not is_login:
        response_data = {'isValid': False, 'VC': 'None'}
        print("返回给前端的数据:")
        print(json.dumps(response_data, indent=4))
        print("========== holderRequestVC 函数执行完毕 ==========\n")
        return jsonify(response_data)
    else:
        conn = sqlite3.connect('accounts.db')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT VC FROM VC')
            vc_document_tuple = cursor.fetchone()
            vc_document = vc_document_tuple[0]
        except Exception as e:
            print(e)
            conn.close()
            response_data = {'isValid': False, 'VC': 'None'}
            return jsonify(response_data)


        conn.close()

        response_data = {'isValid': True, 'VC': vc_document}
        print("返回给前端的数据:")
        print(json.dumps(response_data, indent=4))
        print("========== holderRequestVC 函数执行完毕 ==========\n")
        return jsonify(response_data)


@app.route('/getBeAskedVPList', methods=['POST'])
@cross_origin()
def getBeAskedVPList():
    """
    持有者返回 VP 请求给前端.
    """
    print("========== 开始执行 getBeAskedVPList 函数 ==========")
    global is_login
    print("=======================is_login===========================")
    if not is_login:
        response_data = {'isValid': False, 'VC': 'None'}
        print("返回给前端的数据:")
        print(json.dumps(response_data, indent=4))
        print("========== getBeAskedVPList 函数执行完毕 ==========\n")
        return jsonify(response_data), 401
    else:
        conn = sqlite3.connect('accounts.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT username, datetime FROM AskedVP''')
        data = cursor.fetchall()
        conn.close()

        response_data = {'isValid': True, 'VC': data}
        print("返回给前端的数据:")
        print(json.dumps(response_data, indent=4))
        print("========== getBeAskedVPList 函数执行完毕 ==========\n")
        return jsonify(response_data), 200


@app.route('/holderToVerifier', methods=['POST'])
@cross_origin()
def holderToVerifier():
    """
    持有者生成VP发给验证者
    """
    print("========== 开始执行 holderToVerifier 函数 ==========")
    data = request.json
    print("接收到前端的数据:")
    print(json.dumps(data, indent=4))

    verify_user_name = data.get('username')
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM VC''')
    vc = cursor.fetchone()[0]
    vp_document = generateVP(vc)
    cursor.execute('''
                SELECT ip_address FROM AskedVP WHERE username = ?
            ''', (verify_user_name,))
    ip_addr = cursor.fetchone()[0]

    cursor.execute('''
            DELETE FROM AskedVP WHERE username = ?
            ''', (verify_user_name,))
    conn.commit()

    global flask_port
    port = flask_port
    conn.close()
    url = f'http://{ip_addr}:{port}/getVP'
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, json=vp_document)
        print("发送给验证者的数据:")
        print(json.dumps(vp_document, indent=4))
        print("验证者响应:")
        print(response.text)
        response_data = {'isValid': True}
        print("返回给前端的数据:")
        print(json.dumps(response_data, indent=4))
        print("========== holderToVerifier 函数执行完毕 ==========\n")
        return jsonify(response_data), 200
    except Exception as e:
        print(e, "handle VP failed")
        response_data = {'isValid': False}
        print("返回给前端的数据:")
        print(json.dumps(response_data, indent=4))
        print("========== holderToVerifier 函数执行完毕 ==========\n")
        return jsonify(response_data), 200


@app.route('/recVerifyRequest', methods=['POST'])
@cross_origin()
def recVerifyRequest():
    """
    持有者就收验证者请求存到数据库
    """
    print("========== 开始执行 recVerifyRequest 函数 ==========")
    data = request.json
    print("接收到前端的数据:")
    print(json.dumps(data, indent=4))

    verify_username = data.get('verify_username')
    datetime = data.get('datetime')
    ip_addr = data.get('ip_addr')

    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO AskedVP (username, datetime, ip_address)
        VALUES (?, ?, ?)
    ''', (verify_username, datetime, ip_addr))
    conn.commit()
    cursor.close()

    print("数据已存入数据库")
    print("========== recVerifyRequest 函数执行完毕 ==========\n")
    return jsonify({"isValid": True})


being_verified_vp = None


@app.route('/getVP', methods=['POST'])
@cross_origin()
def getVP():
    """
    验证者接收VP
    """
    print("========== 开始执行 getVP 函数 ==========")
    global being_verified_vp
    being_verified_vp = request.json
    print("接收到的VP数据:")
    print(json.dumps(being_verified_vp, indent=4))
    print("========== getVP 函数执行完毕 ==========\n")
    return jsonify({"isValid": True})


@app.route('/checkVP', methods=['POST'])
@cross_origin()
def checkVP():
    """
    返回给验证者前端 VP
    """
    print("========== 开始执行 checkVP 函数 ==========")
    global being_verified_vp
    if being_verified_vp:
        response_data = {'vp': being_verified_vp}
        print("返回给前端的数据:")
        print(json.dumps(response_data, indent=4))
        print("========== checkVP 函数执行完毕 ==========\n")
        return jsonify(response_data)
    else:
        return jsonify({'vp': ''})


@app.route('/verifyVP', methods=['POST'])
@cross_origin()
def verifyVP():
    """
    验证者验证VP
    """
    print("========== 开始执行 verifyVP 函数 ==========")
    global being_verified_vp
    if being_verified_vp:
        lld = verifyVP(being_verified_vp)
        response_data = {'msg': lld}
        print("返回给前端的数据:")
        print(json.dumps(response_data, indent=4))
        print("========== verifyVP 函数执行完毕 ==========\n")
        return jsonify(response_data)


def get_current_time():
    # 获取当前时间，使用 UTC 时区
    now = datetime.now(timezone.utc)
    # 格式化为 ISO 8601 字符串
    iso8601_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return iso8601_time


@app.route('/askHolder', methods=['POST'])
@cross_origin()
def askHolder():
    """
    验证者给给持有者发送请求
    """
    print("========== 开始执行 askHolder 函数 ==========")
    data = request.json
    print("接收到前端的数据:")
    print(json.dumps(data, indent=4))

    verify_username = data.get('verify_username')
    global flask_port, flask_ip_addr
    ip_addr = flask_ip_addr
    port = flask_port
    info = {
        'verify_username': verify_username,
        'datetime': get_current_time(),
        'ip_addr': ip_addr
    }
    url = f'http://{ip_addr}:{port}/recVerifyRequest'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=info)

    print("发送给持有者的数据:")
    print(json.dumps(info, indent=4))
    print("持有者响应:")
    print(response.text)
    print("========== askHolder 函数执行完毕 ==========\n")
    return jsonify({"isValid": True})


being_verified_did = None


@app.route('/recDID', methods=['POST'])
@cross_origin()
def recDID():
    """
    颁发者接收DID
    """
    print("========== 开始执行 recDID 函数 ==========")
    print("接收到的DID数据:")
    global being_verified_did
    being_verified_did = request.json
    print(json.dumps(being_verified_did, indent=4))
    print("========== recDID 函数执行完毕 ==========\n")
    return jsonify({'isValid':True})


@app.route('/getWhoRequestVerifyDID', methods=['POST'])
@cross_origin()
def getWhoRequestVerifyDID():
    """
    颁发者把DID发给前端
    """
    print("========== 开始执行 getWhoRequestVerifyDID 函数 ==========")
    global is_login
    if not is_login:
        response_data = {'isValid': False, 'username': '', 'DID': ''}
        print("返回给前端的数据:")
        print(json.dumps(response_data, indent=4))
        print("========== getWhoRequestVerifyDID 函数执行完毕 ==========\n")
        return jsonify(response_data)
    else:
        global being_verified_did
        if being_verified_did:
            did = being_verified_did['id']
            response_data = {'isValid': True, 'username': did, 'DID': being_verified_did}
            print("返回给前端的数据:")
            print(json.dumps(response_data, indent=4))
            print("========== getWhoRequestVerifyDID 函数执行完毕 ==========\n")
            return jsonify(response_data)
        else:
            response_data = {'isValid': False, 'username': '', 'DID': ''}
            return jsonify(response_data)


def registerDID(algorithm):
    """
    注册DID
    """
    print("========== 开始执行 registerDID 函数 ==========")
    global contract_addr
    type_of_key = []
    type_of_key.append(algorithm)
    print("选择的算法类型:", type_of_key)
    public_key_pem = []
    private_key_pem = []
    from web3src.generate_key import generate_keys
    for type in type_of_key:
        sk, pk = generate_keys(type)
        public_key_pem.append(pk)
        private_key_pem.append(sk)
    from web3src.interact_with_contract import register_did
    try:
        did_document = register_did(w3, abi, account_addr, contract_addr, public_key_pem, type_of_key,
                                    private_key_pem[0])
    except Exception as e:
        print("注册DID失败:", e)
    else:
        print("======================DID====================")
        print(json.dumps(did_document, indent=4))
        # 这里返回给前端一个did_document，然后数据库就找里面对应的字段就可以，[公私钥对就是前面的两个list，记得加一个type_of_key]，
        # 然后还得再存一份did_document完整的
        conn = sqlite3.connect('accounts.db')
        cursor = conn.cursor()
        did = did_document["id"]
        kid = 1
        # 遍历组合后的数据并插入到数据库中
        cursor.execute('''
            INSERT INTO key (kid, DID, type_of_key, public_key_pem, private_key_pem)
            VALUES (?, ?, ?, ?, ?)
        ''', (kid, did, type_of_key[0], public_key_pem[0], private_key_pem[0]))
        conn.commit()
        conn.close()

        print("DID和密钥对已存入数据库")
        print("========== registerDID 函数执行完毕 ==========\n")
        return json.dumps(did_document)


# 和颁发者交互
@app.route('/requestVerifyDID', methods=['POST'])
@cross_origin()
def requestVerifyDID():
    """
    颁发者验证DID
    """
    print("========== 开始执行 reqeustVerifyDID 函数 ==========")
    data = request.get_json()  # 这里的data是一整个DID document的json，这里应该不能直接传，用json - string 转一下就行
    print("接收到前端的数据:")
    print(json.dumps(data, indent=4))

    global contract_addr, w3, abi
    from web3src.verify_did import verify_did  # 导入verify_did模块

    lld = verify_did(w3, abi, contract_addr, data['DID'])
    print("================VERIFY_DID=============")
    print(lld)

    response_data = {'isValid': lld}
    print("返回给前端的数据:")
    print(json.dumps(response_data, indent=4))
    print("========== reqeustVerifyDID 函数执行完毕 ==========\n")
    return jsonify(response_data)  # 返回给前端login函数那样的jsonfy信息


@app.route('/giveVCToHolder', methods=['POST'])
@cross_origin()
def giveVCToHolder():
    """
    颁发者颁发VC
    """
    data = request.get_json()

    print("========== 开始执行 giveVCToHolder 函数 ==========")
    kid = data.get('kid')
    kid_int = int(ord(kid) - ord('0'))
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()

    # 获取issuer
    cursor.execute('SELECT DID FROM key WHERE kid = 1')
    issuer_tuple = cursor.fetchone()
    issuer = issuer_tuple[0]

    key_id = issuer + '#key-' + kid
    credential_subject = data.get('credential_subject')
    vc_type = data.get('vc_type')

    cursor.execute('SELECT private_key_pem FROM key WHERE kid = ?', (kid_int,))
    private_key_pem_tuple = cursor.fetchone()
    private_key_pem = private_key_pem_tuple[0]  # 提取元组中的第一个元素

    cursor.execute('SELECT type_of_key FROM key WHERE kid = ?', (kid_int,))
    signature_algorithm_tuple = cursor.fetchone()
    signature_algorithm = signature_algorithm_tuple[0]  # 提取元组中的第一个元素

    vc = generate_vc(vc_type, issuer, credential_subject, key_id, private_key_pem, signature_algorithm)
    print("===================VC========================")
    print(json.dumps(vc, indent=4))  # 返回一个vc，显示到前端，然后放在数据库

    vc_id = vc["id"]
    vc_string = json.dumps(vc)
    print(type(vc_string))
    print("=======================================")
    print(vc_string)
    cursor.execute('''
                    INSERT INTO VC (VC) 
                    VALUES (?)
                ''', (vc_string,))
    conn.commit()
    conn.close()

    response_data = {'isValid': True, 'vc': vc}
    print("返回给前端的数据:")
    print(json.dumps(response_data, indent=4))
    print("========== giveVCToHolder 函数执行完毕 ==========\n")
    return jsonify(response_data)

def generateVP(verifiableCredential):
    """
    持有者生成VP
    """
    print("========== 开始执行 generateVP 函数 ==========")
    kid = '1'
    kid_int = int(ord(kid) - ord('0'))
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()

    cursor.execute('SELECT DID FROM key WHERE kid = ?', (kid_int,))
    did = cursor.fetchone()[0]

    key_id = did + '#key-' + kid
    vp_type = 'VerifiablePresentation'

    cursor.execute('SELECT private_key_pem from key WHERE kid = ?', (kid_int,))
    private_key_pem = cursor.fetchone()[0]
    cursor.execute('select type_of_key from key WHERE kid = ?', (kid_int,))
    signature_algorithm = cursor.fetchone()[0]

    from web3src.generate_vp import generate_vp
    ver = []
    ver.append(verifiableCredential)
    vp = generate_vp(vp_type, ver, private_key_pem, signature_algorithm, key_id)
    print("========== generateVP 函数执行完毕 ==========\n")
    return vp


def verifyVP(data):
    """
    验证者验证VP
    """
    print("========== 开始执行 verifyVP 函数 ==========")
    # 获取请求数据
    print("接收到的VP数据:")
    print(json.dumps(data, indent=4))

    global w3, abi, contract_addr
    from web3src.verify_vp import verify_vp
    lld = verify_vp(w3, abi, contract_addr, data)
    print("===================VERIFY_VP================")
    print(lld)
    return lld


if __name__ == '__main__':
    init_func()
    app.run(debug=True, port=5000)
