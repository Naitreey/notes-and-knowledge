cron
====
- Etymology: cron 名字与 chronology 同源, 即希腊语中表示时间的词. chronos.

crontab
=======
overview
--------
- crontab is a file containing instructions to cron(8) daemon.

ownership
---------
- Each user has their own crontab
 
- commands in any given crontab will be executed as the user who owns the
  crontab.

format
------
- Blank lines and leading spaces and tabs are ignored.

- Line comment: Lines whose first non-space character is ``#``. 
  
  * comments are not allowed on the same line as cron commands, since they will
    be taken to be part of the command.

  * comments are not allowed on the same line as environ settings.

- active lines:

  * environment setting

  * cron command

- parsing order: top-down. any environment settings will affect only the cron
  commands below them in the file.

environment settings
^^^^^^^^^^^^^^^^^^^^
::

  name=value

- ``=`` may be surrounded by optional space characters.

- The value string may be placed in quotes (single or double) to preserve
  leading or trailing blanks.

- Environmental substitutions or replacement of variables are NOT parsed.

- predefined environs:

  * SHELL, default /bin/sh

  * LOGNAME. owner, according to /etc/passwd.

  * HOME. default is home of owner, according to /etc/passwd.

  * PATH. default /usr/bin:/bin

  * MAILTO. users to email, separated by comma. default is owner. Set to empty
    string to disable sending email.

  * CONTENT_TYPE, content type of email.
    
  * CONTENT_TRANSFER_ENCODING. ditto.

  * environment defined in /etc/environment, /etc/security/pam_env.conf

cron command
^^^^^^^^^^^^
line format
"""""""""""
user cron command line::

  m h dom m dow command... \n

system cron command line::

  m h dom m dow user command... \n

- The fields may be separated by spaces or tabs.

- The maximum permitted length for the command field is 998 characters.

- 注意 newline at the end of crontab is required.

field format
""""""""""""
- field domains:

  * minute: [0, 59]

  * hour: [0, 23]

  * day of month: [1, 31]

  * month: [1, 12], or names

  * day of week: [0, 7], or names. Note 0 and 7 is Sunday.

- For any field, its value can be

  - A number in domain

  - Range of numbers: ``m-n``. ``*`` stands for full range: first-last.

  - Range of numbers with step: ``<range>/step``

  - A list of numbers or ranges, separated by comma: m-n,o,p.

  - For month and day of week, The first three letters of the month or weekday,
    case-insensitive.
  
- Date and time matching rule. Commands are executed when

  * the minute, hour, and month of year fields match the current time

  * For two day fields (day of month, or day of week):

    - When at least one of the two day fields contains restricted value (not
      ``*``) and the restricted value match the current time.

    - When both day fields contain ``*``, then match all.

- special date time value::

    @reboot        Run once, at startup
    @yearly        0 0 1 1 *
    @annually      same as @yearly
    @monthly       0 0 1 * *
    @weekly        0 0 * * 0
    @daily         0 0 * * *
    @midnight      same as @daily
    @hourly        0 * * * *

command format
""""""""""""""
- The entire command portion of the line, up to a newline or % character, will
  be executed by SHELL.

  * The % in command will be changed into newline characters, and all data
    after the first % will be sent to the command as standard input.

  * Multiline command is not allowed.

language implementations
========================
croniter
--------
- a python module to provide iteration for datetime object.

- 它支持秒级的 crontab.

- supported format::

    m h dom m dow [s]

  注意到 optional seconds 作为第 6 列.

references
==========
- crontab(5)
