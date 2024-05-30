from flask import Flask
from DeCert.routes.did_routes import did_bp

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(did_bp, url_prefix='/did')

if __name__ == '__main__':
    app.run(debug=True)
