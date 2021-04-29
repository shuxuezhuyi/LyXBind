LyXBind
=======

在下为 LyX 设置的快捷键

最直接的用法是, 在 LyX 的首选项中选取 main.bind 为快捷键文件.

lyx.ahk 是 AutoHotkey 脚本. 请到 https://autohotkey.com/ 下载安装 AutoHotkey 以使用它.

用 template.lyx 新建文档以充分利用这些快捷键. 此后生成 tex(XeTeX) 文档后, 可以用 macros.py 展开宏, 从而避免合并别人的文档时发生宏定义的冲突. 用法是: `python3 macros.py 你的tex文件`
