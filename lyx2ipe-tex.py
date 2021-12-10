#!/usr/bin/python3
# sudo apt-get install xclip
# pip3 install pyperclip

from os.path import expanduser
import pyperclip

with open(expanduser('~/.ipe/lyx2ipe.tex'), 'r', encoding='utf-8') as tex: lines = tex.readlines()
write_lines = []
write_sign = False
for line in lines:  # 这个循环截取 LaTeX 文档的正文
    if not write_sign:
        if r'\begin{document}' in line: write_sign = True
        continue
    elif r'\end{document}' in line: break
    write_lines.append(line)
paste = ''.join(write_lines)  # 把多行文本做成一个字符串
pyperclip.copy(paste)  # 复制到系统剪贴板