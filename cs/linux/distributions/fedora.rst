* Pros

  - RHEL, CentOS upstream, 接近 production system

  - 软件更新比较及时

* Cons

  - gnome, kde app 兼容性问题

    * okular crash, 最贱的是在保存文件时崩溃, 甚至导致整个 gui 卡死, 系统卡死,
      除了重启没有办法, 丢失所有当前未保存的修改, 丢失所有正在处理的任务, 打开的
      terminal, 打开的网页, 我操你怎么不去死.

    * ktouch not working

  - gnome 自身的各种 bugs

    * 极偶尔的 gnome-shell crash

    * keyboard layout 无法全局应用, 设置困难.
      localectl, setxkbmap, gsettings 都不能完全修改布局, 叫人无从下手.

  - wayland 尚有诸多限制, 目前没有 xorg 的 customizability 强.
    登录时需要设置为使用 xorg.

    * xdotool 仅有部分功能可用, 例如向指定窗口和位置发点击等操作, 但
      无法发送 key 值, 几乎残废.

