#!/usr/bin/python3
# 用 pip3 install PyUserInput 来安装 pykeyboard，不要用 pip3 install pykeyboard ！

from pykeyboard import *

class ShortcutForLyX(PyKeyboardEvent):
    def __init__(self):
        PyKeyboardEvent.__init__(self)
        self.SingleAlt = 0  # PreventSingleAlt 要用
        self.kbd = PyKeyboard()
        
    def PreventSingleAlt(self, character, press):   # 本意是想阻止LyX响应单按Alt的事件, 但现在只是绕弯子消除影响而已
        if (character == 'Alt_L' or character == 'Alt_R'):
            if press == True:
                if self.SingleAlt == 0: self.SingleAlt =+ 1
                else: self.SingleAlt = 0
            elif self.SingleAlt == 1:
                self.kbd.tap_key(self.kbd.alt_key)  # 抢在下次键盘事件之前触发一次按下Alt键又松开的事件
                self.SingleAlt =+ 1
        else: self.SingleAlt = 0

    def tap(self, keycode, character, press):
        self.PreventSingleAlt(character, press)
        print(keycode, character, press)
        
    def escape(self, event):    # 不用escape退出脚本
        print('no escape')

sample = ShortcutForLyX()
sample.run()