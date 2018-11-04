Virtualization 分类
===================

- full virtualization.

- os-level virtualization.

QEMU/KVM 与 virtualbox 比较
===========================

  不同的应用场景使用不同的 hypervisor 工具.

  * 使用场景: 个人 PC 上使用, 只是开一两个虚拟机平时用一用. 追求简单, 快捷, 方便,
    易用. 应该选择 virtualbox.

  * 使用场景: 大批量部署和维护, 要求自动化, 具有扩展性和二次开发和丰富的接口.
    应该使用 QEMU + KVM + libvirt.

  virtualbox 是 type-2 hypervisor. 即 guest OS 是 host OS 上的一个进程.
  QEMU/KVM 是两个不同的 hypervisor 的搭配. QEMU 是 type-2, KVM 作为 kernel module
  是 type-1. KVM 相对 virtualbox 具有一定速度优势. 并且 QEMU/KVM 更加底层, 可编程
  性更强大. virtualbox 相对上层, 是直接面向终端用户的.

