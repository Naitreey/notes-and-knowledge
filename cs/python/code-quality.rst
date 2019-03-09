vulture
=======
overview
--------
- 用于寻找一个项目中有定义但无使用的函数、变量等代码, 即 dead code.

caveats
-------
- Due to Python's dynamic nature, static code analyzers like Vulture are likely to
  
  * miss some dead code.
    
  * code that is only called implicitly may be reported as unused.

usage
-----
::

  vulture [options] PATH [PATH ...]

- path can be Python files or directories. For each directory Vulture analyzes
  all contained ``*.py`` files.

- each chunk of dead code is assigned a confidence value. A confidence value of
  100% means that the code will never be executed. Values below 100% are only
  estimates for how likely it is that the code is unused.

- options:

  * ``--make-whitelist`` automatically make whitelist for false positives::

      vulture --make-whitelist [PATH] >whitelist.py

    A whitelist is a python file that simulate the usage of variables,
    attributes, etc.

  * ``--exclude PATTERNS``. Comma-separated list of path patterns to ignore.
    Patterns may contain file globs (``*, ?, [abc], [!abc]``). A PATTERN
    without glob wildcards is treated as ``*PATTERN*``.

  * ``--ignore-decorators PATTERNS``. Ignore functions and classes using these
    decorators. PATTERNS are also file globs, as above.

  * ``--ignore-names PATTERNS``. Ignore those name patterns when found as
    unused. PATTERNS ditto.

  * ``--min-confidence CONFIDENCE``.

Marking unused variables as necessary
-------------------------------------
There are situations where you can't just remove unused variables, e.g., in
tuple assignments or function signatures. Vulture will ignore these variables
if they start with an underscore.

Mechanism
---------
Vulture uses the ast module to build abstract syntax trees for all given files.
While traversing all syntax trees it records the names of defined and used
objects. Afterwards, it reports the objects which have been defined, but not
used. This analysis ignores scopes and only takes object names into account.

exit codes
----------
useful for automated CI.

0, no dead code.

1, dead code found, or invalid input.

2, invalid cli usage.
