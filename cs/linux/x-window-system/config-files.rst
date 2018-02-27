xprofile
========
files:

- ~/.xprofile

- /etc/xprofile

由 display manager 去 source, 在进入 X user session 时, 启动 window manager
之前 source.

这些文件都是 shell script.

常见的 display manager 都会 source xprofile 文件, 例如 gdm, kdm, lightdm, lxdm,
sddm.

若不是通过 display manager 而是通过 CLI (startx/initx) 启动, 需要在 xinitrc
中手动添加 source 这些文件.
