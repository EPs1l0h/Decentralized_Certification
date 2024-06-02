# 从Ganache输出文件中读取地址和私钥
def read_ganache_accounts():
    accounts = []
    with open('../ganache_output.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        addr_lines = [line for line in lines if '(100 ETH)' in line]
        key_lines = [line for line in lines if 'Private Keys' not in line and '0x' in line and '(100 ETH)' not in line]
        for addr_line, key_line in zip(addr_lines, key_lines):
            addr = addr_line.split()[1]
            private_key = key_line.split()[1]
            accounts.append((addr, private_key))
    return accounts
