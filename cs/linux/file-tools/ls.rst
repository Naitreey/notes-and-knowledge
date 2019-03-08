output coloring
===============
- ``ls`` output coloring is controlled by ``LS_COLORS`` environ.

dircolors
=========
- dircolors 根据 dir_colors database 输出 ``LS_COLORS`` 环境变量.

read dir_colors database
------------------------
- To read dir_colors database into current shell, use the following

  .. code:: sh

    eval "$(dircolors -b /path/to/database)"

- ~/.bashrc 里一般包含读取并加载 LS_COLORS 数据库的代码. 根据以下优先级递减:

  * ~/.dir_colors
  
  * /etc/DIR_COLORS
  
  * dircolors 命令 hardcoded settings, in its text area.

database format
---------------
- several statements, one per line.

- line comment: starting with ``#``, the hash mark should be at the beginning
  of a line or is preceded by at least one whitespace.

- blank lines are ignored.

- Statements are case-insensitive.

- global section.

  * any statement before the first TERM statement.

  * Any statement in the global section of the file is considered valid for all
    terminal types.

- terminal-specific sections.

  * following the global section.

  * led by one or more TERM statements.

  * statements in terminal-specific section override statements in global
    section.

- statements.

  * ``TERM <terminal-type>`` starts a terminal-specific section. Multiple TERM
    statements can be used to create a section which applies for several
    terminal types.

  * ``NORMAL <color-sequence>``, ``NORM <color-sequence>``. color for normal
    nonfilename text.

  * FILE. regular file.

  * DIR. directories.

  * LINK, LNK, SYMLINK. symlink.

  * ORPHAN. orphaned symlink. fallback to LINK.

  * MISSING. the nonexistent file a orphaned symlink pointing to. fallback to
    FILE.

  * FIFO, PIPE. named pipe.

  * SOCK. socket.

  * DOOR. a solaris door.

  * BLK, BLOCK. a block device file.

  * CHR, CHAR. a character device file.

  * EXEC. a file with exec bits set.

  * SUID, SETUID. a file with setuid bit set.

  * SGID, SETGID. a file with setgid bit set.

  * STICKY. a dir with sticky bit set, but not other-writable.

  * STICKY_OTHER_WRITABLE, OWT. a dir with sticky bit set and other-writable.

  * OTHER_WRITABLE, OWR. a dir without sticky bit set and other-writable.

  * ``*extension <color-sequence>`` for file ending in extension, 注意只需末尾
    match 即可. 这是 file glob pattern.

  * ``.extension <color-sequence>`` 类似上面, 但必须以 period 分割, period is
    included in extension.

  * LEFTCODE, LEFT. left code for ISO 6429 terminal. default ``\e[``

  * RIGHTCODE, RIGHT. right code for ISO 6429 terminal. default ``m``

  * ENDCODE, END. end code for non-ISO 6429 terminal. default undefined.

- for color sequence definitions, see `/cs/linux/terminal/coloring.rst`_.

references
==========
- dir_colors(5)
- `How do I change the color for directories with ls in the console? <https://askubuntu.com/q/466198/348299>`_
