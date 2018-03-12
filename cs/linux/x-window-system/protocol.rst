X resources
===========
X resources are configuration parameters for X client applications.

At the X protocol level, resources are strings that are stored in the server
and have no special meaning. The syntax and meaning of these strings is given
by client libraries and applications.

Resources are manipulated by the xrdb program. In particular, many X display
server configurations run xrdb at start up, instructing it to read the
resources from the .Xresources file in the user's home directory.

syntax
------
- A fully specified resource has the following format::

    application.component.subcomponent.subcomponent.attribute: value

Resources can also be specified for classes of elements.

- value can be integer, boolean (true/false, yes/no, on/off), string.

- wildcard matching:

  - ``?``: match the application name or a single component.
    
  - ``*``: match any number of components.
  
  An attribute part cannot be replaced by a wildcard character.

- comment: ``!`` line.

- include files. 使用 cpp 语法. ``#include "..."``.
