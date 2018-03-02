feature
=======
- powerline 支持 vim, zsh, bash, tmux, ipython, awesome wm, i3 wm, qtile.

requirement
============
- AUR powerline package.

- terminal emulator: true colorr support, fontconfig support or patched font support.

- patched fonts. This is prefered over fontconfig method. Fontconfig method may
  cause alignment issue between powerline symbols and normal font symbols.

configuration
=============
配置文件的位置和自定义规则
--------------------------

- package builtin configurations: ``powerline/config_files``

- user config: ``$XDG_CONFIG_HOME/powerline``

- per instance config.

multiple configuration files that have the same name, but are placed in
different directories, will be merged. Merging happens in the order given in
the above list. When merging configuration only dictionaries are merged and
they are merged recursively.

配置文件的种类
--------------
在每个配置文件位置 ``$CONFDIR``, 可以包含以下配置文件:

main configuration file
~~~~~~~~~~~~~~~~~~~~~~~
- ``$CONFDIR/config.json``

- main config file 主要包含两方面内容:

  * common: 全局配置

  * ext: 对每个 extension, 指定所使用的 colorscheme, theme, 在特定情况下
    使用的 local theme, 以及一些 extension-specific 的基础配置.

具体 key 含义:

- ``colorscheme`` key 决定使用的 colorscheme ``name``.

- ``theme`` & ``top_theme`` keys 决定下述 theme 配置如何构建.
  ``local_themes`` & ``top_theme`` keys 决定在特定情况下的 theme 如何构建.

colorschemes
~~~~~~~~~~~~
This is color scheme definitions, including the following config files:

* ``$CONFDIR/colors.json``. 颜色值的定义.

* ``$CONFDIR/colorschemes/<name>.json``. 名为 name 的 colorscheme, 对所有
  extensions 的通用配置.

* ``$CONFDIR/colorschemes/<extension>/__main__.json``.
  对某种 extension (vim, shell, tmux, etc.), 所有 colorschemes 的通用配置.

* ``$CONFDIR/colorschemes/<extension>/<name>.json``.
  对某种 extension, 某种 colorscheme 的专有配置.

一套完整的 colorscheme 由 ``<name>.json``, ``<extension>/__main__.json``,
``<extension>/<name>.json`` merge 而成. 对于每个文件, 由不同位置的同名文件
merge 而成.

themes
~~~~~~
这是对 segments 功能和布局的配置, 包含以下配置文件:

* ``$CONFDIR/themes/<top_theme>.json``.
  每个 top theme 定义一组 powerline 可以显示的 segments, 配置参数等.
  在 top theme 中不会设置每个 segment 的位置, 只会提供 segment 定义.

* ``$CONFDIR/themes/<extension>/__main__.json``.
  对某个 extension 的各个 theme 都要包含的通用配置.

* ``$CONFDIR/themes/<extension>/<name>.json``.
  对某个 extension, 名为 name 的 theme 定义. 一般在这里定义各个 segment 的
  布局. 例如 left, right, above 各放置什么 segments, 以及各项的优先级.
  
一套完整的 theme 由以上三种配置文件构成. 对于每种文件, 由不同位置的同名文件
merge 而成.

注意 bash 不支持 right segments, 只能把所有 segments 放在左边.

local configuration overrides
-----------------------------

segments
========
