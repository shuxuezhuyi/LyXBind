# 需要用 Python3 执行

from pathlib import Path
import sys, os, urllib.request, shutil, zipfile

if sys.version_info[0] != 3 :
    print('出错啦! 请使用 Python3 来执行脚本.')
    exit()

here = os.path.dirname(os.path.realpath(__file__))

url = r'https://github.com/otfried/ipe/releases/download/v7.2.24/ipe-7.2.24-win64.zip'
file_name = here + r'\ipe-7.2.24-win64.zip'
if os.path.isfile(file_name) == False:
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        print('正在下载 ipe-7.2.24, 请耐心等待...')
        shutil.copyfileobj(response, out_file)
    print(r'ipe-7.2.24 已下载为 ' + file_name)
else: print(file_name + r'似乎已经存在？将使用现有的文件。')

with zipfile.ZipFile(file_name, 'r') as f:
    f.extractall(path = here)

if os.path.isdir(here + r'\ipe'): shutil.rmtree(here + r'\ipe')
os.rename(here + r'\ipe-7.2.24', here + r'\ipe')
print('已经准备好 ipe-7.2.24。现在可以使用 ipe.py 编译图片文件了。')