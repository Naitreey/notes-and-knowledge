Linux guest
===========

kernel drivers
--------------
The following kernel drivers are required for virtual machine to work.  Linux
需要加载这些驱动, 从而能够 "使用" hypervisor 虚拟出来的一系列特殊的 "硬件" 设
备.

- ``vmw_balloon``. memory management driver. 使用 hypervisor 虚拟的内存设备.

- ``vmw_pvscsi``. 使用 VMware Paravirtual SCSI HBA device. 只有部分 vmware
  产品提供这个设备.

- ``vmw_vmci``. Virtual Machine Communication Interface.

- ``vmwgfx``. VMware Graphics (gfx - graphics). DRM driver for VMware SVGA2
  virtual device.

- ``vmxnet3``. VMware vmxnet3 virtual ethernet NIC. 只有部分 vmware 产品提供
  这个设备.

- ``vsock``. Virtual Socket Protocol implementation.

- ``vmw_vsock_vmci_transport``. VMCI transport for Virtual Socket.

Open-VM-Tools
-------------
对于 linux guest, 安装 Open-VM-Tools (而不是 VMware Tools) 以获得一些便利
的功能, 例如: copy & paste between host/guest, shared folders, 分辨率自动
调整等.

utilities
^^^^^^^^^
- vmtoolsd. main service.

- vmware-checkvm. check vm health (?)

- vmware-toolbox-cmd. contrl command.

- vmware-user. syncing clipboard between host and guest.

- vmware-vmblock-fuse. drag & drop between host and guest through FUSE.

- vmhgfs-fuse. mount vmhgfs shared folder.

- vmware-hgfsclient. show available shared folders.

share folders
^^^^^^^^^^^^^
::

  vmhgfs-fuse -o auto_unmount <host-spec> <mountpoint>

- ``host-spec`` format::

    .host:/[<shared-name>/[<subdirectory>]]

  若不指定 ``shared-name``, 则挂载所有共享目录.

references
==========
- VMware/Installing Arch as a guest
  https://wiki.archlinux.org/index.php/VMware/Installing_Arch_as_a_guest
