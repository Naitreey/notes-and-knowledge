overview
========
- A display manager, or login manager, is typically a graphical user interface
  that is displayed at the end of the boot process in place of the default
  shell. 

- common display managers: LightDM, GDM, SDDM.

loading a DM
============
To enable graphical login, enable the appropriate systemd service.
This will create a ``display-manager.service`` symlink in ``/etc/systemd/system``
that points to the enabled DM service unit file.

login sessions
==============
login sessions 位于 ``/usr/share/xsessions``, 它们是 desktop file format. 执行
相应的 Window manager or DE.

rcfiles
=======
Most display managers source ``/etc/xprofile``, ``~/.xprofile`` and
``/etc/X11/xinit/xinitrc.d/``.
