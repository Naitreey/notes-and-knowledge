- Rofi, like dmenu, will provide the user with a textual list of options where
  one or more can be selected. This can either be, running an application,
  selecting a window or options provided by an external script.

features
========

- type any word in any order to filter

- support for fuzzy-, regex-, and glob matching

- modes: window switcher, application launcher, desktop file application launcher,
  ssh launcher, combi mode.

- extensible using scripts

- themes

- mouse support

modes
=====

window switcher (window)
------------------------
switch between all windows.

commands
~~~~~~~~
- delete-entry. ``shift-delete``. close the window.

- accept-custom. ``shift-enter``

window current desktop (windowcd)
---------------------------------
like window switcher but restrict on current desktop.

application launcher (run)
--------------------------
run any command in PATH. GUI 和 CLI 程序都可以执行. 分别使用 enter 和
shift+enter.

commands
~~~~~~~~
- delete-entry. ``shift-delete``. remove the command from run history.

- accept-custom. ``shift-enter``. run commmand in a terminal. VERY USEFUL.

desktop file application launcher (drun)
----------------------------------------
run an app from freedesktop.org Desktop Entries. Auto starting terminal
applications in a terminal.

ssh launcher (ssh)
------------------
parse ``~/.ssh/config`` to find hosts and ssh into them.

script modes
------------
load modes from custom scripts.

keys (keys)
-----------
show a searchable list of key bindings.

combination mode (combi)
------------------------
combine multiple modes into one view.

configurations
==============
config parameters are the same as cmdline options.

configuration from lowest to highest priority:

- system config ``/etc/rofi.conf``.

- Xresources.

- Rasi theme file.

- Local configuration. Normally, depending on XDG, in ``~/.config/rofi/config``. This
  uses the Xresources format.

- cmdline options.

To get a template config file run:

- in xresources format: ``rofi -dump-xresources``

- in new format: ``rofi -dump-config``

``rofi -h`` 有很多有用的信息, 包括哪些选项是 cmdline only 的, 当前各选项的值, monitor
layout, detected modes, compile-time options, 使用的配置文件.

rofi(1) 中配置分类罗列, 便于查找.

some options to clearify
-------------------------

general
~~~~~~~

- modi.

  custom script modes can be added using form::
    <name>:<script>
  then used anywhere as normal modes.

pattern setting
~~~~~~~~~~~~~~~

- terminal. 设置其他选项中的 ``{terminal}`` pattern 对应的值.

- ssh-client. ``{ssh-client}`` ditto for pattern value.

layout
~~~~~~

- columns. 指的是输出几列选项, 不影响每个选项包含几列信息.

key bindings
~~~~~~~~~~~~
The options starting with -kb are keybindings.

rasi themes
===========
you can download themes from repo and just use it.

rasi: rofi advanced style inforamtion. 很像 css 语法.
不同于 css 的地方也有很多.

default key bindings
====================
除了各个 mode 中专门的 key bindings 之外, 有以下

- For text editing, common bash/emacs key bindings are accepted.

- accept input, common: ctrl-m, enter, ctrl-j.

- select entry, common: ctrl-p/n, up/down, page up/down,

- switch to previous/next mode: ctrl-tab, ctrl-shift-tab.

- use selected item as input text: ctrl-space.

- toggle case-sensitivity: grave.

- Toggle levenshtein sorting: alt+grave.

- take screenshot: alt-shift-s.

所有 key bindings 可以自定义.

case-sensitivity and sorting status is show at top right of panel.
