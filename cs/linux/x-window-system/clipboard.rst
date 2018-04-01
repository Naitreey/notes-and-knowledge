overview
========
- 3 selections (roughly clipboards): PRIMARY, SECONDARY, CLIPBOARD

- 无论哪个 clipboard, text is never "sent" anywhere until it is requested by a
  receiving application. When you select text, the application only claims the
  selection [UnixSE]_. 因此注意 copy/paste 时如果源程序关闭了就不管用了.

- users should only be concerned with PRIMARY and CLIPBOARD. SECONDARY is only
  used inconsistently and was intended as an alternate to PRIMARY. The majority
  of programs for Xorg, including Qt and GTK+ applications, treat the the
  PRIMARY and CLIPBOARD selections in the following way:

  * The CLIPBOARD selection is used for explicit copy/paste commands involving
    keyboard shortcuts or menu items. it behaves like the single-clipboard
    system on Windows. CLIPBOARD selection 还支持在 paste 时指定 MIME data
    format.
    
    这是一般情况下使用的 clipboard buffer.

  * The PRIMARY selection is used for the currently highlighted text, even if it
    is not explicitly copied, and for middle-mouse-click pasting.

tools
=====
CopyQ, greenclip, xclip.

greenclip
---------
a rofi plugin for clipboard.

功能:

- clipboard history.

- synchronize PRIMARY & CLIPBOARD.

一般不需要看见这个 clipboard history, 所以隐藏在 rofi 的非默认 modes 列表里即可.
需要时再调出.

配置文件: ``~/.config/greenclip.cfg``

xclip
-----
a command line utility to interact with X clipboards.  It reads text from
standard in or files and makes it available to other X applications for pasting
as an  X  selection.

大致原理上, 它是自己 owns 了 X selection, with piped in text.

features
^^^^^^^^
- read stdin or files to clipboards

- print clipboard content

- support 3 selections. by default use PRIMARY.

common usage
^^^^^^^^^^^^
注意 options can be abbreviated as long as not ambiguous.

- copy from stdin::

    echo 111 | xclip -sel clip

- copy from file::
    
    xclip -sel clip file1 file2

- print CLIPBOARD::

    xclip -sel clip -o

references
==========
.. [UnixSE] `Explaining X11 clipboards <https://unix.stackexchange.com/a/213843/91981>`_
.. [ArchWikiClipboard] `Clipboard <https://wiki.archlinux.org/index.php/clipboard>`_
