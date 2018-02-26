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
