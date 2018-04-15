configuration
=============

- create a swap device or swap file.

- edit grub. add kernel parameter for ``resume=`` device. For swap file, additional
  ``resume_offset=`` is needed. regenerate ``grub.cfg``.

- edit ``mkinitcpio.conf``. add ``resume`` hook. regenerate initramfs.
