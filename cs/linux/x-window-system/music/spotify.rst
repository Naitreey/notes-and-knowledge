- official Linux client AUR package spotify

- spotify implements MPRIS2 D-Bus interface which allows external control.
  ``playerctl`` is very useful in this regards. It can be used to control
  spotify client (or any MPRIS player) via commandline.

- spotify 在切换歌曲时会给 dbus 发信息, 所以若有 notification daemon, 自动
  会在桌面上有提示.
