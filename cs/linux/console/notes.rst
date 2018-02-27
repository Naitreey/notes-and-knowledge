fonts
=====

fonts location
--------------
- ``/usr/share/kbd/consolefonts``
  每种字体由名字和尺寸构成. 尺寸部分为 ``<rows>x<columns>`` or ``<column>``.

common operations
-----------------
- show current console font::
    showconsolefont

- set console font::
    setfont <font-name>

keymaps
=======

Keymaps define the connection between the key pressed and the character used by
the computer. 实际上这是 keyboard driver's translation table.

keymaps location
----------------
- ``/usr/share/kbd/keymaps``

common operations
-----------------
- load key mappings::
    loadkeys <keymap-name>

- show key codes sent by each keyboard keys::
    showkey

config file
===========
- vconsole.conf(5)

  * 设置 key maps and font.

  * 由 udev 在 boot 时调用对 virtual console 进行设置.

  * 手动修改或使用 localectl(1) 修改.
