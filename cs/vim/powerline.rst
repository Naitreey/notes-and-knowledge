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
config locations:

- package builtin configurations: ``powerline/config_files``

- user config: ``$XDG_CONFIG_HOME/powerline``

- per instance config.

multiple configuration files that have the same name, but are placed in
different directories, will be merged. Merging happens in the order given in
the above list. When merging configuration only dictionaries are merged and
they are merged recursively.

files: 

- theme files are powerline functionality configurations.

- colorscheme files are color scheme configurations.

themes
------
- bash 不支持 right segments, 只能把所有 segments 放在左边.

segments
========
