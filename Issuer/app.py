import hashlib
import sqlite3
import json
from flask import Flask, request, jsonify
app = Flask(__name__)

w3 = None
abi = None
bytecode = None
account_addr = ''
contract_addr = ''

def init_func():
    from web3src.deploy import run_deploy
    global w3, abi, bytecode, account_addr, contract_addr
    w3, abi, bytecode, account_addr, contract_addr = run_deploy()

# 和持有者交互 - 注册
@app.route('/register', methods=['POST'])
def register():
    # data = request.get_json()
    # 处理注册逻辑
    # 这里和数据库交互，从ganache_output.txt里面拿addr和私钥（上链用的是interact_with_contract.py里面的函数）
    data = request.json
    account = data.get('account')
    password = data.get('password')
    password_confirm = data.get('password_confirm')

    if password != password_confirm:
        return jsonify({"message": "Registration Failed"}), 401

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
        return jsonify({'private_key': private_key, 'addr': addr, 'did': did}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/registerDID', methods=['POST'])
def registerDID():
    global contract_addr
    # data = request.json
    # type_of_key = data.get('type_of_key') # 一个list，每项用来选择SM2 or RSA
    type_of_key = ['SM2']
    public_key_pem = []
    private_key_pem = []
    from web3src.generate_key import generate_keys
    for type in type_of_key:
        sk, pk = generate_keys(type)
        public_key_pem.append(pk)
        private_key_pem.append(sk)
    from web3src.interact_with_contract import register_did
    did_document = register_did(w3, abi, account_addr, contract_addr, public_key_pem, type_of_key, private_key_pem[0])
    print("======================DID====================")
    print(did_document)
    # 这里返回给前端一个did_document，然后数据库就找里面对应的字段就可以，[公私钥对就是前面的两个list，记得加一个type_of_key]，
    # 然后还得再存一份did_document完整的


# 和颁发者交互
@app.route('/verifyDID', methods=['POST'])
def verifyDID():
    # data = request.get_json()  # 这里的data是一整个DID document的json，这里应该不能直接传，用json - string 转一下就行
    # data = json.loads(data)
    data = {
        "@context": ["https://www.w3.org/ns/did/v1"],
        "id": "did:dc:9648a072c53748223360c5c5186927b517b0afbc",
        "created": "2024-06-02T17:35:49Z",
        "updated": "2024-06-02T17:35:49Z",
        "version": "1.0",
        "verificationMethod": [
            {
                "id": "did:dc:9648a072c53748223360c5c5186927b517b0afbc#key-1",
                "type": "SM2",
                "publicKeyPem": """
    -----BEGIN PUBLIC KEY-----
    MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE+opacF908xjq6d2/kpjpeZd/PM2Q
    YWNL0MmQB4xgtI1ZO6Fd8kccP44xrWtQ71SSOTUj/brd5MZzGvHjKjNjAQ==
    -----END PUBLIC KEY-----
    """,
                "address": "0x9648A072C53748223360C5c5186927B517b0aFBC"
            }
        ],
        "proof": {
            "type": "SM2",
            "created": "2024-06-02T17:35:49Z",
            "proofPurpose": "assertionMethod",
            "verificationMethod": "did:dc:9648a072c53748223360c5c5186927b517b0afbc#key-1",
            "proofValue": "3046022100905d0d292bd2d82ab0914e54812cfb01215623d551c06d1da6a62022bb2e83ee022100dbafb6b1e4fc15d64f3d39c44b8ef40e2491c23268233aac1a85e1384ac4379e"
        }
    }
    global contract_addr, w3, abi
    from web3src.verify_did import verify_did  # 导入verify_did模块

    lld = verify_did(w3, abi, contract_addr, data)
    print(lld)
    return lld # 返回给前端login函数那样的jsonfy信息

@app.route('/generateVC', methods=['POST'])
def generateVC():
    # data = request.get_json()
    # credential_subject = data.get('credential_subject') # 声明
    # vc_type = data.get('vc_type') # VC类型
    # kid = data.get('kid') # 采用第几个公私钥对进行签名
    kid = '1'
    issuer = 'did' #从数据库拿自己的did
    key_id = issuer + '#key-' + kid
    credential_subject = 'I can play football'
    vc_type = 'AlumniCredential'
    private_key_pem = '-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCOU0dxNFY/+BtR\nGxN+lYZ+HGD8oN3XvkC2we/CffHJeY2GLAOxSY+f7anc8m9P3//jX0NN2h9Nc1p4\nzBXNt9sitDjnPtaBaMA7iyiDc/Q9gMxkaNWeCKdXkyC34zVM8NUBNWLpjF6feWc7\nwBgIEphHZGemQYTc5NOOTe++iEiqm1Et8cjbydNAkEn9/i/uqvil1A+TE8OxaCC2\nyNQrov2Gdix2d5+xiInwcfbbX7y8quTUxBw/J8D8Vx/QmGya8aj2lGxlUflXZEul\nZ5NplbWIMfohCygb/pmSSUAkrMH9CjuPO6tDK8jJ8//LpxEHsdbEXvQdIgwjBLQB\nXLiFEh+XAgMBAAECggEADWUZHDZox6x6Ja/+rbM07TmOhzg8qMlnHcwy3IMt9mBS\nSYZq8oyRz+N2US0f/MyAMM4Ob41P1OI+aZALnUjofuOnV1w6pANP1ErMjVKkcgVl\nNy4GrNDzrvJR6fygT5V69ponrQNhBHFQnfb+TAQ0AMQaXTNdZczDfGkpXy1EaYoA\nrXtSP2YXaIPSmke6IheP062Qmy7EowlLDVjkHp+QqQA9pcVQC6NYy/7bsGsVr5IX\nGzxskBwfMjuwlnJn16kadmEJHLUYRfHuzegiNx0CE9az/HwaxYyaN9SNHmt8oKSe\nmOKaobTEOOy+0ctdblEqVvC5sH05uHRDNqxGdY/uwQKBgQDGIRzI7chXNqQagfk9\nGbkFVCwnu242rIu9Bl86qEauoJbJAmZTdqR0nOJwY4/U6rJY28ij6vdpY75ziinq\ndlIK4EeGoEZofoj3WTqLgbDv+4Gi12obwoXWvzGK7JtEKunuUMfO6ZpSMuNZEeRp\nGGOh6pw2jafdOlhxSUeslV6jNQKBgQC35XxbdXZpK6f9F/rN5nkCdUrB9Y5Q2HQ1\nl62bMYbWrWOYVGa4xDaThwpkTF3DhJ2frHeo8zSv/GtmIHSOV7fEn/NE02WsR6pS\npN+pToZsh1gGzXGZEHMgRlw75wa9Zn6hr0uJ03NVe3dC1+KQSld56Og8BBErBU/N\nY28lwkdlGwKBgB3OL2letAvCsY83TEpPy1Cs5/OWM69P57mo8rx9QhzVFbnpfYFC\n0NymGT51C9co82mArr9SAqQ9GBKDj2ixIgh20uvCwrTHjE1BhBgmi3qeqFLZ+yFv\n8vhqTMasb3MizYxHZLeQ1uFUvHTSxzy0KZDbHWLrjnwuYc2xC3JACjudAoGBAK3q\nXr2wTRgRrYHy18M6oF7uxpDAxqM20lCM7ibDpB4LRRGfYLaE+ohzQiSxBEwQc3G7\nDj++Iqn9MyUWtKSZ2LYf/1WsB4/zBuW5/7yDAyZIqbtlOHXl1LtFT51nVDxzXndS\n7UGftIe3iIay3RZQ+IHW/ysjPYlOMLaxv0AaiKLZAoGARXlf770aqdV2N0cTJVuH\nnf+0iYpIqkpELoNv7FrvA0epP5ZcBDb0BWONurzcRxVEkGBidA5jwT11C/hdsZhW\nRp+hzl+Lyz5uaCi9YyZC3PZypoGOJhWKKaq9dgAaWzpdrFzhL9zwOc1Xd9KHz6Jd\nCtTfwG+7YXw4Bb+TxN4N1A8=\n-----END PRIVATE KEY-----\n'
    signature_algorithm = 'RSA' # 从数据库拿
    from web3src.generate_vc import generate_vc
    vc = generate_vc(vc_type, issuer, credential_subject, key_id, private_key_pem, signature_algorithm)
    print("===================VC========================")
    print(vc) # 返回一个vc，显示到前端，然后放在数据库


# 和验证者交互 - 验证VC
@app.route('/verifyVC', methods=['POST'])
def verifyVC():
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
    global w3, abi, contract_addr
    from web3src.verify_vc import verify_vc
    lld = verify_vc(w3, abi, contract_addr, data)
    print(lld)
    return lld # 返回jsonfy信息

@app.route('/generateVP', methods=['POST'])
def generateVP():
    # data = request.get_json()
    # vp_type = data.get('vp_type') # VP类型
    # kid = data.get('kid') # 采用第几个公私钥对进行签名
    # verifiableCredential = data.get('verifiableCredential') # 一个vc list，这里json-string可能有问题
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
    verifiableCredential = [data]
    kid = '1'
    did = 'did:example:ebfeb1f712ebc6f1c276e12ec21' #从数据库拿
    key_id = did + '#key-' + kid
    vp_type = 'VerifiablePresentation'
    private_key_pem = '-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCOU0dxNFY/+BtR\nGxN+lYZ+HGD8oN3XvkC2we/CffHJeY2GLAOxSY+f7anc8m9P3//jX0NN2h9Nc1p4\nzBXNt9sitDjnPtaBaMA7iyiDc/Q9gMxkaNWeCKdXkyC34zVM8NUBNWLpjF6feWc7\nwBgIEphHZGemQYTc5NOOTe++iEiqm1Et8cjbydNAkEn9/i/uqvil1A+TE8OxaCC2\nyNQrov2Gdix2d5+xiInwcfbbX7y8quTUxBw/J8D8Vx/QmGya8aj2lGxlUflXZEul\nZ5NplbWIMfohCygb/pmSSUAkrMH9CjuPO6tDK8jJ8//LpxEHsdbEXvQdIgwjBLQB\nXLiFEh+XAgMBAAECggEADWUZHDZox6x6Ja/+rbM07TmOhzg8qMlnHcwy3IMt9mBS\nSYZq8oyRz+N2US0f/MyAMM4Ob41P1OI+aZALnUjofuOnV1w6pANP1ErMjVKkcgVl\nNy4GrNDzrvJR6fygT5V69ponrQNhBHFQnfb+TAQ0AMQaXTNdZczDfGkpXy1EaYoA\nrXtSP2YXaIPSmke6IheP062Qmy7EowlLDVjkHp+QqQA9pcVQC6NYy/7bsGsVr5IX\nGzxskBwfMjuwlnJn16kadmEJHLUYRfHuzegiNx0CE9az/HwaxYyaN9SNHmt8oKSe\nmOKaobTEOOy+0ctdblEqVvC5sH05uHRDNqxGdY/uwQKBgQDGIRzI7chXNqQagfk9\nGbkFVCwnu242rIu9Bl86qEauoJbJAmZTdqR0nOJwY4/U6rJY28ij6vdpY75ziinq\ndlIK4EeGoEZofoj3WTqLgbDv+4Gi12obwoXWvzGK7JtEKunuUMfO6ZpSMuNZEeRp\nGGOh6pw2jafdOlhxSUeslV6jNQKBgQC35XxbdXZpK6f9F/rN5nkCdUrB9Y5Q2HQ1\nl62bMYbWrWOYVGa4xDaThwpkTF3DhJ2frHeo8zSv/GtmIHSOV7fEn/NE02WsR6pS\npN+pToZsh1gGzXGZEHMgRlw75wa9Zn6hr0uJ03NVe3dC1+KQSld56Og8BBErBU/N\nY28lwkdlGwKBgB3OL2letAvCsY83TEpPy1Cs5/OWM69P57mo8rx9QhzVFbnpfYFC\n0NymGT51C9co82mArr9SAqQ9GBKDj2ixIgh20uvCwrTHjE1BhBgmi3qeqFLZ+yFv\n8vhqTMasb3MizYxHZLeQ1uFUvHTSxzy0KZDbHWLrjnwuYc2xC3JACjudAoGBAK3q\nXr2wTRgRrYHy18M6oF7uxpDAxqM20lCM7ibDpB4LRRGfYLaE+ohzQiSxBEwQc3G7\nDj++Iqn9MyUWtKSZ2LYf/1WsB4/zBuW5/7yDAyZIqbtlOHXl1LtFT51nVDxzXndS\n7UGftIe3iIay3RZQ+IHW/ysjPYlOMLaxv0AaiKLZAoGARXlf770aqdV2N0cTJVuH\nnf+0iYpIqkpELoNv7FrvA0epP5ZcBDb0BWONurzcRxVEkGBidA5jwT11C/hdsZhW\nRp+hzl+Lyz5uaCi9YyZC3PZypoGOJhWKKaq9dgAaWzpdrFzhL9zwOc1Xd9KHz6Jd\nCtTfwG+7YXw4Bb+TxN4N1A8=\n-----END PRIVATE KEY-----\n'
    signature_algorithm = 'RSA' # 从数据库拿
    from web3src.generate_vp import generate_vp
    vp = generate_vp(vp_type, verifiableCredential, private_key_pem, signature_algorithm, key_id)
    print("====================VP=======================")
    print(vp) # 返回一个vc，显示到前端，然后放在数据库


# 和验证者交互 - 验证VP
@app.route('/verifyVP', methods=['POST'])
def verifyVP():
    # 获取请求数据
    # json_string = request.get_json()
    # data = json.loads(json_string) # 一个vp
    data = {
        "@context": ["https://www.w3.org/2018/credentials/v1", "https://www.w3.org/2018/credentials/examples/v1"],
        "type": "VerifiablePresentation",
        "verifiableCredential": [
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
        ],
        "proof": {
            "type": "RSA",
            "created": "2024-06-02T19:49:18.225987+00:00",
            "proofPurpose": "authentication",
            "verificationMethod": "did:example:ebfeb1f712ebc6f1c276e12ec21#key-1",
            "challenge": "9ab31b6e-7dae-4ab2-a532-202d9382b341",
            "domain": "example.com",
            "proofValue": "62eebf56bf63421b0143ed59f317ff4ddd3bceb29c355878e05af6b1db3d2d80f4cbae15f80b454965fc6211baee0e2bf7b96a18fc1b637e34634a2fe821194427638d155ad0b114cc739ba2423de5224add4075b17288d8841899eef2454891852db64dff58b547649b8e768de8b786fbc0b823e1cba9e7cfa7445111c20b7fada2dc118b192e08f88ce7768b44a676cb2faed587859e2b99b5c42b4488e203fc37eb4251f6ce5640cd14f40529b009fad0fe9a67b6f43d8dfb30db576ba544870fefcaa998c8196113153e1f0db494e5194bd17cc5d890912501059f0e02ea36c62f5981013c08ca5c813f1fabdda0be61daa387b111ac3dfab350ea899b61"
        }
    }
    global w3, abi, contract_addr
    from web3src.verify_vp import verify_vp
    lld = verify_vp(w3, abi, contract_addr, data)
    print(lld)
    return lld # 返回jsonfy

if __name__ == '__main__':
    init_func()
    # 把下面函数的注释去掉，再把app.run注释掉可以调试运行
    registerDID()
    verifyDID()
    generateVC()
    verifyVC()
    generateVP()
    verifyVP()
    # app.run(debug=True)
