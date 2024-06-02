from flask import Flask, request, jsonify

app = Flask(__name__)

# 和持有者交互
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # 处理注册逻辑
    # 这里和数据库交互，从ganache_output.txt里面拿addr和私钥（上链用的是interact_with_contract.py里面的函数）
    # 返回

    return jsonify({"message": "Register endpoint"}), 200

# 和持有者交互
@app.route('/login', methods=['POST'])
def register():
    data = request.get_json()
    # 处理登录逻辑
    # 这里和数据库交互，从ganache_output.txt里面拿addr和私钥（上链用的是interact_with_contract.py里面的函数）
    # 返回

    return jsonify({"message": "Register endpoint"}), 200


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
        from verify_did import verify_did  # 导入verify_did模块
    finally:
        sys.path.pop(0)  # 无论如何，最后都恢复sys.path

    # 调用verify_did函数
    b_dir = os.path.dirname(os.path.abspath(__file__))
    c_path = os.path.join(b_dir, 'web3src\\contract_address.txt')
    with open (c_path,'r') as file:
        contract_address = file.read()
    lld = verify_did(contract_address, data)
    return lld

# 和验证者交互
@app.route('/verifyVC', methods=['POST'])
def verifyVC():
    # 获取请求数据
    data = request.get_json()
    from web3src.verify_vc import verify_vc
    lld = verify_vc(data['vc'],) # 这里是不是得根据需要改一下？
    # 处理VC验证逻辑
    # ...
    return lld

# 和验证者交互
@app.route('/verifyVP', methods=['POST'])
def verifyVP():
    # 获取请求数据
    data = request.get_json()
    from web3src.verify_vp import verify_vp
    lld = verify_vp(data['vp'],) # 这里是不是得根据需要改一下？
    # 处理VC验证逻辑
    # ...
    return lld

if __name__ == '__main__':
    app.run(debug=True)
