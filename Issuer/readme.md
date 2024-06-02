# readme

## 需要注意的点：

- 每次重置记得检查addr，有两个addr，一个是服务器的，这个我应该都写了在文件夹里自动化了；另一个是用户的addr，这个你们来维护，目前的测试样例都是用的写死的


### [ 标识符注册机构 ] 使用方法（请严格按照使用顺序，理论上运行路径无关，建议命令行运行）

- 运行web3.py，会启动ganache链，并将账号密码信息提取出来，并放入文件，

- 运行deploy.py，重新执行后相当于重新部署合约

- 运行app.py，启动标识符注册机构

- src/test/testld 这个是和app的交互示例，验证DID/VC/VP可以用这里面的函数（验证DID的已经跑通，其它的可以构造示例试一下）验证者的后端直接用这个即可

- verify_did.py等verify的函数开箱即用，已经测试完成，输入格式也已经给了


