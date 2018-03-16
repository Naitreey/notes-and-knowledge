- 解压时文件权限问题.

  * for non-root: 默认是 ``--no-same-owner`` & ``--no-same-permissions``.
    即, 解压时修改文件 owner 为自己, permission 应用 user's umask 进行修改.

  * for root: 默认是 ``--same-owner`` & ``--same-permissions``.
    即保持 archive 中保存的 owner 和 permission 原样不变.
  
  因此, tarball 中一定要避免包含 root directory 本身, 例如 ``/etc/some/conf``,
  而是仅包含相对路径 ``etc/some/conf``. 这样, 在相对于 root directory
  提取时, 不会覆盖 root directory. 注意此时解压一般是用 root, 所以如果 archive
  中 / 权限和 owner 不对, 会被覆盖错. 导致系统无法使用.

  一般地, 也要注意 archive 中包含的重要系统目录的 owner/permission 情况,
  避免导致一些系统目录的权限被错误修改.
