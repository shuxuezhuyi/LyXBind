#!/usr/bin/python3
# 此脚本仅限 Linux 使用. 目前仅在 Debian 11 (bullseye) + Python 3.9.2 + PyUserInput 0.1.11 + pynput 1.7.5 + LyX 2.3.6 + Ipe 7.2.23 中测试
# 先启动 LyX, 再加载本程序
# 用 pip3 install PyUserInput 来安装 pykeyboard，不要用 pip3 install pykeyboard ！
# pip3 install pynput
# sudo apt-get install wmctrl  # 我发现 wmctrl 比 xdotool 更擅长跳转窗口
# sudo apt-get install xdotool  # 有时候 PyUserInput 并没有正常运行, 于是需要 xdotool, 特别是在跳转窗口之后
# sudo apt-get install xclip  # pyperclip 依赖它
# pip3 install pyperclip  # 调用系统剪贴板

from pykeyboard import *
from pynput.mouse import Button, Controller  # 我没有使用 pynput 来监控键盘, 因为我不明白 pynput 为什么要用守护线程, 而且我也不懂得用守护线程
from os import popen
from collections import deque
from os.path import expanduser

# 辅助快捷键
class Shortcuts(PyKeyboardEvent):
    def __init__(self):
        PyKeyboardEvent.__init__(self)  # 一个监控键盘事件的线程
        self.kbd = PyKeyboard()  # 模拟键盘
        self.m = Controller()  # 模拟鼠标
        self.active = 'LyX' # 默认活动窗口是 LyX
        self.KeySequence = deque([['', '', False], ['', '', True], ['', '', False]], maxlen=4) # 记录最近四次按键事件
        self.SingleAlt = 0  # PreventSingleAlt 要用
        self.CreateOrEdit = 'Create text object'  # Ipe 编辑文本的窗口有两个名称
        popen(r'lyx -n ~/.ipe/lyx2ipe.lyx') # 请确保已经手动创建一个合适的 ~/.ipe/lyx2ipe.lyx, 并确保是一个独立的 LyX 进程打开它. 千万不要在这个 LyX 进程中打开别的文档, 以免发生意外. 请取消勾选 LyX 中的选项 "只开启一个 LyX 实例"
        
    def PreventSingleAlt(self, character, press):   # 本意是想阻止LyX响应单按Alt的事件, 但现在只是绕弯子消除影响而已
        if character == 'Alt_L' or character == 'Alt_R':
            if press == True:
                if self.SingleAlt == 0: self.SingleAlt =+ 1
                else: self.SingleAlt = 0
            elif self.SingleAlt == 1:
                self.kbd.tap_key('Alt_L')  # 抢在下次键盘事件之前触发一次按下Alt键又松开的事件
                self.SingleAlt =+ 1
        else: self.SingleAlt = 0
        
    def 返回Ipe(self): # 在 LyX 里使用快捷键 F9 返回 Ipe
        if self.KeySequence[-2][-2:] == ['F9', True] and self.KeySequence[-1][-2:] == ['F9', False]:
            self.KeySequence.append(['', '', False])  # 清除状态
            self.kbd.press_keys(['Control_R', 's'])  # 保存
            popen(r'lyx -batch -e xetex ~/.ipe/lyx2ipe.lyx; python3 ~/lyx/LyXBind/lyx2ipe-tex.py; wmctrl -a "' + self.CreateOrEdit + r'"; xdotool key --clearmodifiers ctrl+a Delete ctrl+v BackSpace keyup ctrl')  # 先导出 LaTeX 文档, 再把它的正文复制到剪贴板, 然后返回 Ipe 粘贴. 需要用 keyup ctrl 是因为 xdotool 不一定会释放 ctrl 键.
        
    def IpeMouse(self):  # 在 Ipe 里把 3 当鼠标左键用，把 2 当鼠标右键用
        if self.KeySequence[-1][-2:] == ['3', True]: self.m.press(Button.left)
        elif self.KeySequence[-1][-2:] == ['3', False]: self.m.release(Button.left)
        elif self.KeySequence[-1][-2:] == ['2', True]: self.m.press(Button.right)
        elif self.KeySequence[-1][-2:] == ['2', False]: self.m.release(Button.right)
        
    # Ipe 就算能正常召唤外部编辑器又如何? 并没有多实用. 不如我自己用快捷键 Alt+l 直接开 LyX 
    def EditInLyX(self):
        keys = list(self.KeySequence)
        if (keys[-4] == ['Ipe编辑文本的窗口', 'Alt_L', True] or keys[-4] == ['Ipe编辑文本的窗口', 'Alt_R', True]) \
        and keys[-3] == ['Ipe编辑文本的窗口', 'l', True] \
        and [keys[-2][0], keys[-1][0], keys[-2][2], keys[-1][2]] == ['Ipe编辑文本的窗口', 'Ipe编辑文本的窗口', False, False]:
            self.KeySequence.append(['', '', False])  # 清除状态
            popen(r'xdotool key --clearmodifiers BackSpace ctrl+a ctrl+c keyup ctrl; wmctrl -a "~/.ipe/lyx2ipe.lyx"; xdotool key --clearmodifiers ctrl+a ctrl+p click 1 keyup ctrl')  # 转到编辑 ~/.ipe/lyx2ipe.lyx 的 LyX 窗口, 并把刚才复制的文本当作 LaTeX 粘贴进来覆盖原有的文本. 最后点击鼠标左键是为了激活窗口, 但如果窗口本身不是最大化的话, 可能会出意外.
            # wmctrl 切换时窗口标题没有标注 LyX, 是因为文档有改动时 LyX 的窗口标题中会多一个*
            
    def tap(self, keycode, character, press):  # 主循环，检测到 character 的 press 状态，然后处理
        a = popen('/usr/bin/xdotool getactivewindow getwindowname').read() # 注意最后有换行符 \n
        #print(a)  # 用来看活动窗口是什么
        if a.startswith('Ipe '):
            if self.active != 'Ipe':
                self.KeySequence.append(['', '', False])  # 清除状态
                self.active = 'Ipe'
        elif a.endswith(' LyX\n'):
            if self.active != 'LyX':
                self.KeySequence.append(['', '', False])  # 清除状态
                self.active = 'LyX'
        elif a == 'Create text object\n' or a == 'Edit text object\n':
            if self.active != 'Ipe编辑文本的窗口':
                self.KeySequence.append(['', '', False])  # 清除状态
                self.active = 'Ipe编辑文本的窗口'
                self.CreateOrEdit = a[:-1]
        else:
            self.active = ''
            self.KeySequence.append(['', '', False])  # 在别的活动窗口里仅仅清除状态, 别的什么也不要做
        self.KeySequence.append([self.active, character, press])
        if self.active == 'LyX':
            self.PreventSingleAlt(character, press)
            if a.startswith('~/.ipe/lyx2ipe.lyx'): self.返回Ipe()
        elif self.active == 'Ipe': self.IpeMouse()
        elif self.active == 'Ipe编辑文本的窗口': self.EditInLyX()
        #print(keycode, character, press)  # 用来看被检测到的是什么
        
    def escape(self, event):    # 不用escape退出脚本，咱有Ctrl+C就可以啦；这个循环会在 tap 之前执行
        return False

S = Shortcuts()
S.run()
