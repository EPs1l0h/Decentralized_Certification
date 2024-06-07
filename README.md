# readme
## 代码运行
### 后端
```shell
conda create -n caa python=3.8 -y
conda activate caa
pip install -r requirements.txt

npm install -g ganache-cli
cd Issuer/web3src
python compileSolidity.py # 编译合约，需要开梯子并且大概1分钟

```
打开一个新的终端开启ganache-cli，开启区块链服务，不要中断
```shell
cd Issuer
ganache-cli
```
再打开一个新的终端运行后端程序
```shell
cd Issuer
python app.py
```
### 前端
打开一个新的终端安装并运行前端
```shell
cd ca-frontend
npm install
npm run serve
```

## 代码介绍
