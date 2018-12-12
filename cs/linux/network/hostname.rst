systemd
=======
在 systemd 的系统中, hostname 的设置逻辑大致是这样:

* 在启动阶段:

  - initramfs 阶段使用镜像里保存的 `/etc/hostname`, 这是之前 `dracut` 做镜像
    时包含在里面的.

  - chroot 后, systemd 启动 systemd-hostnamed.service, 后者通过以下顺序决定
    hostname:

    * 使用 `/etc/hostname`.

    * 通过 `/etc/machine-info` 里的 `PRETTY_HOSTNAME` 推出一个 hostname.

    * 通过 IP 地址请求 reverse DNS 给出给出一个 "transient hostname".

    * 使用默认的 `localhost`.

* 在运行阶段:
  用户可使用 `hostnamectl`, 通过 systemd-hostnamed.service 来控制 hostname,
  以及各种其他标识信息.
