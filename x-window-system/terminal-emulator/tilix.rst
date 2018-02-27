installation
============
- AUR tilix or tilix-bin package. tilix-bin package seems easier.
  At present, vte3-notification AUR package also needs to be built for notification etc.

features
========

main features
-------------
- windows

- sessions

- tabs

- password manager

- bookmark

- open file browser at cwd

- save terminal output to file

- advanced paste dialog

- save/restore session.

- key bindings

badge
-----
ok, what's the ponit.

command line actions
--------------------
use command line actions to have the running instance execute an action that
you would typically do through the user interface.

- open new terminal with profile

- set title of new terminal tab

- restore saved sessions. Useless as process is not saved.

- create tab or session in current terminal.

- create new terminal maximized/minimized/full-screen/with specified dimension.

- create new terminal in guake mode.

- open preference

custom hyperlink
----------------
regex matching output content and associate actions to it.

The token $0 refers to the complete regular expression match. If groups were
defined in the regular expression, the tokens $1, $2, $3, etc refer to the
individual group captures.

automatic profile switching
---------------------------
based on:

- username

- hostname

- cwd

guake mode
----------
not interested.

paramter substitution in titles
-------------------------------

triggers
--------
A trigger consists of a regular expression, the action to execute and a
parameter string. The result of the regular expression can be referenced as
tokens in the parameter.

The token $0 refers to the complete regular expression match. If groups were
defined in the regular expression, the tokens $1, $2, $3, etc refer to the
individual group captures.


vte config
==========
description
-----------
One aspect of VTE configuration is the use of /etc/profile.d/vte.sh. The VTE
uses this script to override the PROMPT_COMMAND in order to feed itself
additional information via terminal control codes.

different distributions treat /etc/profile.d differently. The expectation is
that when a shell is initiated all scripts in /etc/profile.d are executed. On
Fedora, this works as expected for both login and non-login based shells.
However, other distributions (Ubuntu and Arch at least) only execute scripts
in /etc/profile.d for login shells.

two issues:

- The current directory is never reported by VTE. This means when splitting
  terminals in Tilix instead of inheriting the directory from the current
  terminal the split terminal always opens in your home terminal. Gnome
  Terminal has the same issue when creating new tabs

- The Fedora patched VTE that provides notification support depends on
  PROMPT_COMMAND, so this issue means notifications will not work.

solution
--------
use login shell.
