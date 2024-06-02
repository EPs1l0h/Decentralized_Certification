import os
import re

# 临时文件名
output_file = 'ganache_output.txt'

# 启动Ganache并将输出重定向到临时文件
os.system(f'ganache > {output_file} 2>&1')

# 读取输出
with open(output_file, 'r', encoding='utf-8') as file:
    output = file.read()

# 检查Ganache是否成功启动
if "Starting RPC server" in output:
    print("Ganache started successfully.")
else:
    print("Failed to start Ganache.")
    print(output)
    exit(1)

# 解析账户和私钥
accounts = re.findall(r'\(\d+\)\s(0x[a-fA-F0-9]{40})\s', output)
private_keys = re.findall(r'\(\d+\)\s(0x[a-fA-F0-9]{64})', output)

# 将用户账号和私钥存入list
account_private_key_pairs = list(zip(accounts, private_keys))

# 打印账户和私钥列表
for i, (account, private_key) in enumerate(account_private_key_pairs):
    print(f"Account {i}: {account}, Private Key: {private_key}")

# 删除临时文件
os.remove(output_file)
