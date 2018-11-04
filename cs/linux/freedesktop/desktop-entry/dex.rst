overview
========
- ``dex`` is a program to execute and generate DesktopEntry files of the
  Application type.

execute
=======
::

  dex [OPTIONS] [<desktop-file>]

- ``--autostart``. execute autostart programs (in ``/etc/xdg/autostart`` and
  ``~/.config/autostart``).

- ``--search-paths <paths>``. a colon-separated list of pathes to search for
  desktop files.

- ``--environment NAME[=VALUE]``

create
======
::

  dex --create <path> [<desktop-file>]

- ``--create <path>``.

- ``--target-directory <dir>``. create in that directory.

other options
=============
- ``--dry-run``. e.g.:

  .. code:: sh

    dex -ad # preview programs to autostart
    dex -ad -e GNOME

references
==========
- dex(1)

- github repo

- How can I use autostart .desktop files in i3?
  https://faq.i3wm.org/question/2155/how-can-i-use-autostart-desktop-files-in-i3.1.html
