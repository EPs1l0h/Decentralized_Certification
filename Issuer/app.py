import hashlib
import sqlite3
import json
import os
from datetime import datetime, timezone

from web3 import Web3
from flask import Flask, request, jsonify
import requests

from web3src.generate_vc import generate_vc

app = Flask(__name__)

w3 = None
abi = None
bytecode = None
account_addr = ''
contract_addr = ''
user_name = ''
is_login = False
flask_ip_addr = '10.21.246.227'
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

<<<<<<< Updated upstream
@app.route('/checkUserName', methods=['GET'])
=======

@app.route('/checkUserName', methods=['POST'])
@cross_origin()
>>>>>>> Stashed changes
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
def register():
    """
    data = request.get_json()
    处理注册逻辑
    这里和数据库交互，从ganache_output.txt里面拿addr和私钥（上链用的是interact_with_contract.py里面的函数）
    """
    print("========== 开始执行 register 函数 ==========")
    data = request.json
<<<<<<< Updated upstream
=======
    print("接收到前端的数据:")
    print(json.dumps(data, indent=4))

    global is_login, user_name
    user_name = data.get('username')
    is_login = True
>>>>>>> Stashed changes
    password = data.get('password')
    password_confirm = data.get('password_confirm')

    if password != password_confirm:
<<<<<<< Updated upstream
        return jsonify({"message": "Registration Failed"}), 401
    registerDID()
=======
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

>>>>>>> Stashed changes
    # 返回
    response_data = {"message": "Registration Successful"}
    print("返回给前端的数据:")
    print(json.dumps(response_data, indent=4))
    print("========== register 函数执行完毕 ==========\n")
    return jsonify(response_data), 200


# 获取Holder信息
@app.route('/get_holder_info', methods=['GET'])
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


@app.route('holderToVerifier', methods=['POST'])
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
def checkVP():
    """
    返回给验证者前端 VP
    """
    print("========== 开始执行 checkVP 函数 ==========")
    global being_verified_vp
    if being_verified_vp:
<<<<<<< Updated upstream
        return jsonify({'vp': being_verified_vp})
@app.route('verifyVP', methods=['POST'])
=======
        response_data = {'vp': being_verified_vp}
        print("返回给前端的数据:")
        print(json.dumps(response_data, indent=4))
        print("========== checkVP 函数执行完毕 ==========\n")
        return jsonify(response_data)
    else:
        return jsonify({'vp': ''})


@app.route('/verifyVP', methods=['POST'])
@cross_origin()
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
@app.route('/recDID',  methods=['POST'])
=======


@app.route('/recDID', methods=['POST'])
@cross_origin()
>>>>>>> Stashed changes
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


@app.route('/registerDID', methods=['POST'])
def registerDID():
    """
    注册DID
    """
    print("========== 开始执行 registerDID 函数 ==========")
    global contract_addr
<<<<<<< Updated upstream
    # data = request.json
    # type_of_key = data.get('type_of_key') # 一个list，每项用来选择SM2 or RSA
    type_of_key = ['RSA']
=======
    type_of_key = []
    type_of_key.append(algorithm)
    print("选择的算法类型:", type_of_key)
>>>>>>> Stashed changes
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
@app.route('/reqeustVerifyDID', methods=['POST'])
def reqeustVerifyDID():
    """
    颁发者验证DID
    """
    print("========== 开始执行 reqeustVerifyDID 函数 ==========")
    data = request.get_json()  # 这里的data是一整个DID document的json，这里应该不能直接传，用json - string 转一下就行
    print("接收到前端的数据:")
    print(json.dumps(data, indent=4))
    # data = {
    #     '@context': ['https://www.w3.org/ns/did/v1'],
    #     'id': 'did:dc:0adf883f21794e0a0f4cc274840c295ab617595a',
    #     'created': '2024-06-03T06:33:41Z',
    #     'updated': '2024-06-03T06:33:41Z',
    #     'version': '1.0',
    #     'verificationMethod': [{'id': 'did:dc:0adf883f21794e0a0f4cc274840c295ab617595a#key-1',
    #                             'type': 'SM2',
    #                             'publicKeyPem': '-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEv+VYFHhq+aFEWHp+SSSldxltbUmD\n8AgonywFoMQDxXBo2114qQ11unvJEjTyl1m4tWrDY6UO73WjPHMQU7W3VA==\n-----END PUBLIC KEY-----\n',
    #                             'address': '0x0ADF883f21794E0a0f4cc274840C295ab617595A'}],
    #     'proof': {'type': 'SM2',
    #               'created': '2024-06-03T06:33:41Z',
    #               'proofPurpose': 'assertionMethod',
    #               'verificationMethod': 'did:dc:0adf883f21794e0a0f4cc274840c295ab617595a#key-1',
    #               'proofValue': '30440220680cefe4910599dd119c89029663e0f2a58aae0b3eaf716b4c1ee2e04726a69d02201ec4c64943092df18c2f280ddc2b09f4e1ad29d5d1d015d5b12dc763850f6276'}
    # }

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
def giveVCToHolder():
    """
    颁发者颁发VC
    """
    data = request.get_json()
    # credential_subject = data.get('credential_subject') # 声明
    # vc_type = data.get('vc_type') # VC类型
    # kid = data.get('kid') # 采用第几个公私钥对进行签名

    # private_key_pem = '-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCOU0dxNFY/+BtR\nGxN+lYZ+HGD8oN3XvkC2we/CffHJeY2GLAOxSY+f7anc8m9P3//jX0NN2h9Nc1p4\nzBXNt9sitDjnPtaBaMA7iyiDc/Q9gMxkaNWeCKdXkyC34zVM8NUBNWLpjF6feWc7\nwBgIEphHZGemQYTc5NOOTe++iEiqm1Et8cjbydNAkEn9/i/uqvil1A+TE8OxaCC2\nyNQrov2Gdix2d5+xiInwcfbbX7y8quTUxBw/J8D8Vx/QmGya8aj2lGxlUflXZEul\nZ5NplbWIMfohCygb/pmSSUAkrMH9CjuPO6tDK8jJ8//LpxEHsdbEXvQdIgwjBLQB\nXLiFEh+XAgMBAAECggEADWUZHDZox6x6Ja/+rbM07TmOhzg8qMlnHcwy3IMt9mBS\nSYZq8oyRz+N2US0f/MyAMM4Ob41P1OI+aZALnUjofuOnV1w6pANP1ErMjVKkcgVl\nNy4GrNDzrvJR6fygT5V69ponrQNhBHFQnfb+TAQ0AMQaXTNdZczDfGkpXy1EaYoA\nrXtSP2YXaIPSmke6IheP062Qmy7EowlLDVjkHp+QqQA9pcVQC6NYy/7bsGsVr5IX\nGzxskBwfMjuwlnJn16kadmEJHLUYRfHuzegiNx0CE9az/HwaxYyaN9SNHmt8oKSe\nmOKaobTEOOy+0ctdblEqVvC5sH05uHRDNqxGdY/uwQKBgQDGIRzI7chXNqQagfk9\nGbkFVCwnu242rIu9Bl86qEauoJbJAmZTdqR0nOJwY4/U6rJY28ij6vdpY75ziinq\ndlIK4EeGoEZofoj3WTqLgbDv+4Gi12obwoXWvzGK7JtEKunuUMfO6ZpSMuNZEeRp\nGGOh6pw2jafdOlhxSUeslV6jNQKBgQC35XxbdXZpK6f9F/rN5nkCdUrB9Y5Q2HQ1\nl62bMYbWrWOYVGa4xDaThwpkTF3DhJ2frHeo8zSv/GtmIHSOV7fEn/NE02WsR6pS\npN+pToZsh1gGzXGZEHMgRlw75wa9Zn6hr0uJ03NVe3dC1+KQSld56Og8BBErBU/N\nY28lwkdlGwKBgB3OL2letAvCsY83TEpPy1Cs5/OWM69P57mo8rx9QhzVFbnpfYFC\n0NymGT51C9co82mArr9SAqQ9GBKDj2ixIgh20uvCwrTHjE1BhBgmi3qeqFLZ+yFv\n8vhqTMasb3MizYxHZLeQ1uFUvHTSxzy0KZDbHWLrjnwuYc2xC3JACjudAoGBAK3q\nXr2wTRgRrYHy18M6oF7uxpDAxqM20lCM7ibDpB4LRRGfYLaE+ohzQiSxBEwQc3G7\nDj++Iqn9MyUWtKSZ2LYf/1WsB4/zBuW5/7yDAyZIqbtlOHXl1LtFT51nVDxzXndS\n7UGftIe3iIay3RZQ+IHW/ysjPYlOMLaxv0AaiKLZAoGARXlf770aqdV2N0cTJVuH\nnf+0iYpIqkpELoNv7FrvA0epP5ZcBDb0BWONurzcRxVEkGBidA5jwT11C/hdsZhW\nRp+hzl+Lyz5uaCi9YyZC3PZypoGOJhWKKaq9dgAaWzpdrFzhL9zwOc1Xd9KHz6Jd\nCtTfwG+7YXw4Bb+TxN4N1A8=\n-----END PRIVATE KEY-----\n'
    # signature_algorithm = 'RSA' # 从数据库拿

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


# 和验证者交互 - 验证VC
@app.route('/verifyVC', methods=['POST'])
def verifyVC():
    print("========== 开始执行 verifyVC 函数 ==========")
    """
    验证VC，这里不调用了，直接验证VP就行
    """
    # 获取请求数据
    # data = request.get_json() 一整个 vc
    json_string = """
    {
        "@context": "https://www.w3.org/2018/credentials/v1", 
        "id": "DeCertIssuer-d5cbe332-caa8-4ece-adeb-3d50fd81b6aa", 
        "type": ["VerifiableCredential", "AlumniCredential"], 
        "issuer": "epsilon", 
        "issuanceDate": "2024-06-02T18:50:50.996563+00:00", 
        "credentialSubject": "I can play football", 
        "proof": {
            "type": "RSA", 
            "created": "2024-06-02T18:50:51.028577+00:00", 
            "proofPurpose": "assertionMethod", 
            "verificationMethod": "epsilon/keys/1", 
            "proofValue": "2cb1b6ed89b0cec4d49d12691d12285bac9eee26c99e3341bb50d0b82593446dab0bf789d10176fefa836da49ab7732929dafe670d6286a10ed03a595c48b3706aebbeed72a5062b8f62548c6abb49c94efdcea0a54fb17af329fda9ceffc115699b969eb8b86cc59a39808484be630c08a0972ace4c1b22a843f67816596d121321fd1a3038f2f185ef52b03bf9ac32ff22f605ee6b905530b785763fd52feb28125cf6d24d16250bc483b234c1abd682d49ab5489b15ad91471e918e47042799fb1c36e6b63ddae5e46d6b4fc5d7a724d9199d61dd57b4c03c2ec513e8ec9af568d301226df51c3815e55045daa991044d1420cf99d57a06c2566cac2e93f2"
        }
    }
    """
    data = json.loads(json_string)
    print("接收到的VC数据:")
    print(json.dumps(data, indent=4))

    global w3, abi, contract_addr
    from web3src.verify_vc import verify_vc
    lld = verify_vc(w3, abi, contract_addr, data)
    print("===============VERIFY_VC================")
    print(lld)

    print("========== verifyVC 函数执行完毕 ==========\n")
    return lld  # 返回jsonfy信息


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
    # private_key_pem = '-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCOU0dxNFY/+BtR\nGxN+lYZ+HGD8oN3XvkC2we/CffHJeY2GLAOxSY+f7anc8m9P3//jX0NN2h9Nc1p4\nzBXNt9sitDjnPtaBaMA7iyiDc/Q9gMxkaNWeCKdXkyC34zVM8NUBNWLpjF6feWc7\nwBgIEphHZGemQYTc5NOOTe++iEiqm1Et8cjbydNAkEn9/i/uqvil1A+TE8OxaCC2\nyNQrov2Gdix2d5+xiInwcfbbX7y8quTUxBw/J8D8Vx/QmGya8aj2lGxlUflXZEul\nZ5NplbWIMfohCygb/pmSSUAkrMH9CjuPO6tDK8jJ8//LpxEHsdbEXvQdIgwjBLQB\nXLiFEh+XAgMBAAECggEADWUZHDZox6x6Ja/+rbM07TmOhzg8qMlnHcwy3IMt9mBS\nSYZq8oyRz+N2US0f/MyAMM4Ob41P1OI+aZALnUjofuOnV1w6pANP1ErMjVKkcgVl\nNy4GrNDzrvJR6fygT5V69ponrQNhBHFQnfb+TAQ0AMQaXTNdZczDfGkpXy1EaYoA\nrXtSP2YXaIPSmke6IheP062Qmy7EowlLDVjkHp+QqQA9pcVQC6NYy/7bsGsVr5IX\nGzxskBwfMjuwlnJn16kadmEJHLUYRfHuzegiNx0CE9az/HwaxYyaN9SNHmt8oKSe\nmOKaobTEOOy+0ctdblEqVvC5sH05uHRDNqxGdY/uwQKBgQDGIRzI7chXNqQagfk9\nGbkFVCwnu242rIu9Bl86qEauoJbJAmZTdqR0nOJwY4/U6rJY28ij6vdpY75ziinq\ndlIK4EeGoEZofoj3WTqLgbDv+4Gi12obwoXWvzGK7JtEKunuUMfO6ZpSMuNZEeRp\nGGOh6pw2jafdOlhxSUeslV6jNQKBgQC35XxbdXZpK6f9F/rN5nkCdUrB9Y5Q2HQ1\nl62bMYbWrWOYVGa4xDaThwpkTF3DhJ2frHeo8zSv/GtmIHSOV7fEn/NE02WsR6pS\npN+pToZsh1gGzXGZEHMgRlw75wa9Zn6hr0uJ03NVe3dC1+KQSld56Og8BBErBU/N\nY28lwkdlGwKBgB3OL2letAvCsY83TEpPy1Cs5/OWM69P57mo8rx9QhzVFbnpfYFC\n0NymGT51C9co82mArr9SAqQ9GBKDj2ixIgh20uvCwrTHjE1BhBgmi3qeqFLZ+yFv\n8vhqTMasb3MizYxHZLeQ1uFUvHTSxzy0KZDbHWLrjnwuYc2xC3JACjudAoGBAK3q\nXr2wTRgRrYHy18M6oF7uxpDAxqM20lCM7ibDpB4LRRGfYLaE+ohzQiSxBEwQc3G7\nDj++Iqn9MyUWtKSZ2LYf/1WsB4/zBuW5/7yDAyZIqbtlOHXl1LtFT51nVDxzXndS\n7UGftIe3iIay3RZQ+IHW/ysjPYlOMLaxv0AaiKLZAoGARXlf770aqdV2N0cTJVuH\nnf+0iYpIqkpELoNv7FrvA0epP5ZcBDb0BWONurzcRxVEkGBidA5jwT11C/hdsZhW\nRp+hzl+Lyz5uaCi9YyZC3PZypoGOJhWKKaq9dgAaWzpdrFzhL9zwOc1Xd9KHz6Jd\nCtTfwG+7YXw4Bb+TxN4N1A8=\n-----END PRIVATE KEY-----\n'
    # signature_algorithm = 'RSA' # 从数据库拿

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
<<<<<<< Updated upstream
    # 把下面函数的注释去掉，再把app.run注释掉可以调试运行
    registerDID()
    verifyDID()
    generateVC()
    verifyVC()
    generateVP()
    verifyVP()
    # app.run(debug=True)
=======
    app.run(host='10.21.246.227', debug=True, port=5000)
>>>>>>> Stashed changes
