import os
import shutil
import zipfile



def split_dir(path, sign=['/', '\\']):
    if len(sign) < 1:
        sign=['/', '\\']
    for s in sign:
        path = path.replace(s, sign[0])
    result = path.split(sign[0])
    return result
                

def mkdir(path):
    if type(path) == str:
        path = split_dir(path)
    temp_path = ''
    for directory in path:
        temp_path += directory + '/'
        if not is_exist(temp_path):
            os.mkdir(temp_path)
    return temp_path

def rmdir(path):
    try:
        cnt = 0
        for root, dirs, files in os.walk(path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                cnt += 1
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                os.rmdir(dir_path)
                cnt += 1
        os.rmdir(path)
        return cnt
    except Exception as e:
        return e

def is_exist(path):
    if os.path.exists(path):
        return path
    else:
        return None

def write_text(path, text, line = False):
    if os.path.exists(path):
        mode = 'a'
    else:
        mode = 'w'
    if line:
        text += '\n'
    with open(path, mode) as f:
        f.write(text)
    return len(text)

def preprocess_text(text, exception = []):
    result = ''
    for char in text:
        if char.isalpha() or char.isdigit() or char in exception:
            result += char
        elif char.isspace():
            result += ' '
    return result.strip()

def move_file(source_path, destination_path):
    shutil.move(source_path, destination_path)

def unzip_file(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def remove_file(file_path):
    try:
        os.remove(file_path)
        return file_path
    except FileNotFoundError:
        print(f"{file_path} FileNotFoundError.")
        return "ERRNO"
    except PermissionError:
        print(f"{file_path} PermissionError.")
        return "ERRNO"
    except exception as e:
        print(e)
        return e

