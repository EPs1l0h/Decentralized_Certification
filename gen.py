import os

def is_code_file(filename):
    return filename.endswith('.py') or filename.endswith('.html') or filename.endswith('.java') or filename.endswith('.c') or filename.endswith('.cpp') or filename.endswith('.js') or filename.endswith('.ts') or filename.endswith('.vue') or filename.endswith('.properties')
def get_directory_structure(path, prefix=''):
    structure = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            if item not in ['venv', '__pycache__', '.git', 'dist']:  # 排除不需要显示的目录
                structure.append(prefix + '📁 ' + item)
                structure.extend(get_directory_structure(item_path, prefix + '    '))
        elif os.path.isfile(item_path) and is_code_file(item):
            structure.append(prefix + '📄 ' + item)
    return structure

def get_all_files(path):
    all_files = []
    for root, _, files in os.walk(path):
        if any(excluded_dir in root for excluded_dir in ['venv', '__pycache__', '.git','dist']):
            continue

        for file in files:
            if is_code_file(file):
                all_files.append(os.path.join(root, file))
    return all_files

# 指定要处理的目录路径
target_dir = '/Users/wendy/pro/Decentralized_Certification/Issuer'

# 获取目录结构
directory_structure = get_directory_structure(target_dir)

# 获取目录下的所有代码文件
code_files = get_all_files(target_dir)

# 将目录结构和代码文件内容合并到一个文件中,用target_dir的最后一个来命名

filename = target_dir.split('/')[-1] + '_all_code.txt'
#创建文件

with open(filename, 'w') as outfile:
    outfile.write("Here's the directory structure and code files:\n\n")

    # 写入目录结构
    outfile.write("Directory Structure:\n")
    for item in directory_structure:
        outfile.write(item + "\n")
    outfile.write("\n")

    # 写入代码文件内容
    outfile.write("Code Files:\n")
    for fname in code_files:
        relative_path = os.path.relpath(fname, target_dir)
        outfile.write(f"----- Start of {relative_path} -----\n")
        with open(fname) as infile:
            outfile.write(infile.read())
        outfile.write(f"\n----- End of {relative_path} -----\n\n")

print(f'The file {filename} has been created!')

