#!/usr/bin/python3
# 本程序假设被修改文档所在目录为工作目录
# 用法: python3 macros.py your_tex_file
import sys

tex = str(sys.argv[1]) # 第一个参数默认是要修改的文件的名字。也可使用完整的绝对路径。
with open(tex, 'r') as read_file: lines = read_file.readlines()

macros = {} # 用字典储存: 宏 - 宏定义

for line in lines:
    if line.startswith(r'\global\long\def\mathist'):
        m = line.find(r'\mathist')
        l = line.find('{') # 最左边的 {
        r = line.rfind('}') # 最右边的 }
        key = line[m:l]
        value = line[l+1:r]
        macros[key] = value
    elif r'数学宏的定义到此为止' in line: break

write_lines = []
write_sign = False

for line in lines:
    if not write_sign:
        if r'数学宏的定义到此为止' in line: write_sign = True # 直到数学宏的定义结束，都视为 preamble 的内容，不展开宏
        if line.startswith(r'\global\long\def\mathist'): continue # 不再保留数学宏的定义
        write_lines.append(line)
    else: 
        for key, value in macros.items():
            line = line.replace(key, value) # 把每个数学宏替换为它的定义
        write_lines.append(line)
        
with open(tex, 'w') as write_file:
    write_file.writelines(write_lines)