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

yapf
====
overview
--------
- yapf -- yet another python formatter.

- yapf is based off of clang-format and gofmt. In essence, the algorithm takes
  the code and reformats it to the best formatting that conforms to the style
  guide, even if the original code didn't violate the style guide.

- The goal is straightforward: end all holy wars about formatting - if the
  whole codebase of a project is simply piped through YAPF whenever
  modifications are made, the style remains consistent throughout the project
  and there's no point arguing about style in every code review.

- version support: 2.7, 3.6.4+. Run yapf under the interpreter whose version
  matches that of code to be formatted.

usage
-----
::

  yapf [options] [file ...]

- Read from stdin if no files are specified.

- options.

  * ``-d``, ``--diff``, print the diff for the fixed source

  * ``-i``, change in-place

  * ``-r``, run recursively over directories

  * ``-l <start>-<end>``, reformat from "start" line to "end" line. lines are
    1-based.

  * ``-e PATTERN``, exclude files matching PATTERN from being formatted.

  * ``--style STYLE``. the formatting style. See `formatting style`_ for
    detail.

  * ``--style-help``. show style settings and exit. this output can be saved to
    .style.yapf to make your settings permanent

  * ``--no-local-style``. don't search for a local style definition.

  * ``-p``. run yapf in parallel when formatting.

  * ``-vv``, print out file names while processing.

- return code:

  * normally: 0 on success, non-0 otherwise.

  * with ``--diff``, 0 if no changes, non-0 otherwise. can be used in a CI
    workflow to test that code has been YAPF-formatted.

yapfignore
----------
In addition to exclude patterns provided on commandline, YAPF looks for
additional patterns specified in a file named ``.yapfignore`` located in the
working directory from which YAPF is invoked.

formatting style search order
-----------------------------
* specified by the command line option ``--style``.

* In the ``[style]`` section of a ``.style.yapf`` file in either the current
  directory or one of its parent directories.

* In the ``[yapf]`` section of a ``setup.cfg`` file in either the current
  directory or one of its parent directories.

* In the ``~/.config/yapf/style`` file.

* Use pep8 style as default.
  
formatting style
----------------
- ``--style`` option value can be
  
  * a style name. valid style names: pep8, google, Chromium, facebook.
   
  * a path to a file with style settings.

  * a dict of key-value pairs, equivalent to a style config file's content.

- config file format:

  * ini format.

  * keys are case-insensitive.

- config keys. a full list of configuration keys are defined in ``style.py``.

  * ``based_on_style``, which of the predefined styles this custom style is
    based on.

  * ``ALIGN_CLOSING_BRACKET_WITH_VISUAL_INDENT``, Align closing bracket with
    visual indentation. (??)

  * ``ALLOW_MULTILINE_LAMBDAS``, Allow lambdas to be formatted on more than one
    line. (??)

  * ``ALLOW_MULTILINE_DICTIONARY_KEYS``, Allow dictionary keys to exist on
    multiple lines.

      .. code:: python

      x = {
          ('this is the first element of a tuple',
           'this is the second element of a tuple'):
               value,
      }

  * ``ALLOW_SPLIT_BEFORE_DEFAULT_OR_NAMED_ASSIGNS``, Allow splitting before a
    default / named assignment in an argument list. (??)

  * ``ALLOW_SPLIT_BEFORE_DICT_VALUE``. Allow splits before the dictionary
    value.

      .. code:: python

      x = {
          ('this is the first element of a tuple', 'this is the second element of a tuple'):
          value,
      }

      # vs

      x = {
          ('this is the first element of a tuple', 'this is the second element of a tuple'): value,
      }

  * ``ARITHMETIC_PRECEDENCE_INDICATION``. Let spacing indicate operator
    precedence. 


    .. code:: python

      a = 1 * 2 + 3 / 4
      b = 1 / 2 - 3 * 4
      c = (1 + 2) * (3 - 4)
      d = (1 - 2) / (3 + 4)
      e = 1 * 2 - 3
      f = 1 + 2 + 3 + 4

      # vs

      a = 1*2 + 3/4
      b = 1/2 - 3*4
      c = (1+2) * (3-4)
      d = (1-2) / (3+4)
      e = 1*2 - 3
      f = 1 + 2 + 3 + 4

  * ``BLANK_LINE_BEFORE_NESTED_CLASS_OR_DEF``. Insert a blank line before a
    ``def`` or ``class`` immediately nested within another ``def`` or
    ``class``.

    .. code:: python

      class Foo:
                         # <------ this blank line
          def method():
              pass

  * ``BLANK_LINE_BEFORE_MODULE_DOCSTRING``. Insert a blank line before a module
    docstring.

    .. code:: python

      #!/usr/bin/env python
                         # <------ this blank line
      """
      1111
      """
  * ``BLANK_LINE_BEFORE_CLASS_DOCSTRING``.  Insert a blank line before a
    class-level docstring.

    .. code:: python

       class A:
                         # <------ this blank line
           """
           sefsef
           """
       
           def f(self):
               pass

  * ``BLANK_LINES_AROUND_TOP_LEVEL_DEFINITION``.  Sets the number of desired
    blank lines surrounding top-level function and class definitions.

    .. code:: python

      class Foo:
          pass
                         # <------ having two blank lines here
                         # <------ is the default setting
      class Bar:
          pass

  * ``COALESCE_BRACKETS``.  Do not split consecutive brackets. Only relevant
    when ``DEDENT_CLOSING_BRACKETS`` is set.

    .. code:: python

      call_func_that_takes_a_dict(
          {
              'key1': 'value1',
              'key2': 'value2',
          }
      )

      # would reformat to:

      call_func_that_takes_a_dict({
          'key1': 'value1',
          'key2': 'value2',
      })

  * ``COLUMN_LIMIT``.  The column limit (or max line-length)

  * ``CONTINUATION_ALIGN_STYLE`` The style for continuation alignment. (??)
    Possible
    values are:

    - ``SPACE``: Use spaces for continuation alignment. This is default
      behavior.

    - ``FIXED``: Use fixed number (``CONTINUATION_INDENT_WIDTH``) of columns
      (ie: ``CONTINUATION_INDENT_WIDTH``/``INDENT_WIDTH`` tabs) for
      continuation alignment.

    - ``VALIGN-RIGHT``: Vertically align continuation lines with indent
      characters. Slightly right (one more indent character) if cannot
      vertically align continuation lines with indent characters.

    For options ``FIXED``, and ``VALIGN-RIGHT`` are only available when
    ``USE_TABS`` is enabled.

  * ``CONTINUATION_INDENT_WIDTH``.  Indent width used for line continuations.

  * ``DEDENT_CLOSING_BRACKETS``.  Put closing brackets on a separate line,
    dedented, if the bracketed expression can't fit in a single line. Applies
    to all kinds of brackets, including function definitions and calls.

    .. code:: python

      config = {
          'key1': 'value1',
          'key2': 'value2',
      }  # <--- this bracket is dedented and on a separate line

  * ``DISABLE_ENDING_COMMA_HEURISTIC``.  Disable the heuristic which places
    each list element on a separate line if the list is comma-terminated.

    .. code:: python

      a = [
          1, 2, 3, 4, 5,
          6, 7, 8, 9, 10,
      ]

      # whether to format into this

      a = [
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10,
      ]

  * ``EACH_DICT_ENTRY_ON_SEPARATE_LINE``. 当 dict 在一行中放不下时, place each
    dictionary entry onto its own line.

    .. code:: python
      a = {
          "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa": 1,
          "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb": 2, "c": 3, "d": 4
      }

      # vs

      a = {
          "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa": 1,
          "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb": 2,
          "c": 3,
          "d": 4
      }

  * ``I18N_COMMENT``.  The regex for an internationalization comment. The
    presence of this comment stops reformatting of that line, because the
    comments are required to be next to the string they translate.

  * ``I18N_FUNCTION_CALL``.  The internationalization function call names. The
    presence of this function stops reformatting on that line, because the
    string it has cannot be moved away from the i18n comment. (??)

  * ``INDENT_DICTIONARY_VALUE``. 当 value cannot fit on the same line as the
    dictionary key 从而需要放到下一行时, 将 value indent 一下.

    .. code:: python

      a = {
          "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa":
              1,
          "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb":
              2,
          "c":
              3,
          "d":
              4
      }

  * ``INDENT_WIDTH``.  The number of columns to use for indentation.

  * ``INDENT_BLANK_LINES``. 对于需要空出的行, prefer indented blank lines
    rather than empty.

  * ``JOIN_MULTIPLE_LINES``.  Join short lines into one line. E.g., single line
    if statements. (??)

  * ``NO_SPACES_AROUND_SELECTED_BINARY_OPERATORS``.  Do not include spaces
    around selected binary operators.  a string of comma separated list of
    operators.

  * ``SPACES_AROUND_POWER_OPERATOR`` Set to True to prefer using spaces around
    ``**``.

  * ``SPACES_AROUND_DEFAULT_OR_NAMED_ASSIGN``.  Set to True to prefer spaces
    around the assignment operator for default or keyword arguments.

  * ``SPACES_BEFORE_COMMENT``.  The number of spaces required before a trailing
    comment. This can be a single value (representing the number of spaces
    before each trailing comment) or a python list of values (representing
    alignment column values; trailing comments within a block will be aligned
    to the first column value that is greater than the maximum line length
    within the block).  (???)

  * ``SPACE_BETWEEN_ENDING_COMMA_AND_CLOSING_BRACKET``.  Insert a space between
    the ending comma and closing bracket of a list, etc.

    .. code:: python

      a = [1, 2, 3, 4, 5, 6, 7, 8,]
      # vs
      a = [1, 2, 3, 4, 5, 6, 7, 8, ]

  * ``SPLIT_ARGUMENTS_WHEN_COMMA_TERMINATED``.  Split before arguments if the
    argument list is terminated by a comma. (??)

  * ``SPLIT_ALL_COMMA_SEPARATED_VALUES``.  If a comma separated list (dict,
    list, tuple, or function def) is on a line that is too long, split such
    that all elements are on a single line.

    .. code:: python

      a = [1111111111111111111111111,2222222222222222222,3333333333333333333,44444444444444444444,55555555555555555]

      # to this
      a = [
          1111111111111111111111111, 2222222222222222222, 3333333333333333333,
          44444444444444444444, 55555555555555555
      ]

      # vs to this

      a = [
          1111111111111111111111111,
          2222222222222222222,
          3333333333333333333,
          44444444444444444444,
          55555555555555555
      ]

  * ``SPLIT_BEFORE_BITWISE_OPERATOR``.  Set to True to prefer splitting before
    '&', '|' or '^' rather than after.

    .. code:: python

      if (aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa & bbbbbbbbbbbbbbbbbbbbbbb
              & ccccccccccccccc & ddddddddddddddd):
          pass

  * ``SPLIT_BEFORE_ARITHMETIC_OPERATOR``.  Set to True to prefer splitting
    before '+', '-', '*', '/', '//', or '@' rather than after.

    .. code:: python

      a = (bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb+ cccccccccccccccccccc+ddddddddddddddddddd+eeeeeeeeeeeeeeeeeee+ffffffffffffffffffffffffffff)
      # vs
      a = (bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb + cccccccccccccccccccc
           + ddddddddddddddddddd + eeeeeeeeeeeeeeeeeee
           + ffffffffffffffffffffffffffff)

  * ``SPLIT_BEFORE_CLOSING_BRACKET``.  Split before the closing bracket if a
    list or dict literal doesn't fit on a single line.

    .. code:: python

      a = [111111111111111,22222222222222222222222,333333333333333,444444444,5555555]
      # to this
      a = [
          111111111111111, 22222222222222222222222, 333333333333333, 444444444,
          5555555
      ]

      # vs to this

      a = [
          111111111111111, 22222222222222222222222, 333333333333333, 444444444,
          5555555]

  * ``SPLIT_BEFORE_DICT_SET_GENERATOR``. 当 list/set/dict etc. comprehension
    expression 太长时, Split before ``for``.

  * ``SPLIT_BEFORE_DOT``. 当需要 split 一个很长的代码至多行时, 并且能够
    split before dot 时, 就这么做.

    .. code:: python

      a = ("111111111111111111111111111111111111111111111111111111111111111111{}".format(2))
      # to
      a = ("111111111111111111111111111111111111111111111111111111111111111111{}"
           .format(2))

      # vs

      a = ("111111111111111111111111111111111111111111111111111111111111111111{}".
           format(2))

  * ``SPLIT_BEFORE_EXPRESSION_AFTER_OPENING_PAREN``. Split after the opening
    paren which surrounds an expression if it doesn't fit on a single line.
    (??)

  * ``SPLIT_BEFORE_FIRST_ARGUMENT``. If an argument / parameter list is going
    to be split, then split before the first argument.

    .. code:: python

      ffffffffffffffffffffffff(aaaaaaaaaaa, bbbbbbbbbbbbbbbbb, ccccccccccc, 44444444444444)
      # to
      ffffffffffffffffffffffff(aaaaaaaaaaa, bbbbbbbbbbbbbbbbb, ccccccccccc,
                               44444444444444)
      # vs to
      ffffffffffffffffffffffff(
          aaaaaaaaaaa, bbbbbbbbbbbbbbbbb, ccccccccccc, 44444444444444)

  * ``SPLIT_BEFORE_LOGICAL_OPERATOR``. Set to True to prefer splitting before
    and or or rather than after.

    .. code:: python

      if (aaaaaaaaaaaaaaaaaaaaaaaaa and bbbbbbbbbbbbbbbbbb or cccccccccccccc
              and ddddddddddddddddd > eeeeeeeee and not fffffffffffffff):
          pass

  * ``SPLIT_BEFORE_NAMED_ASSIGNS``. Split named assignments onto individual lines.

    .. code:: python

      a = dict(aaaaaaaaaaaaaaaaaaaaaaaaa=11111111111111111111,bbbbbbbbbbbbbbbbbbbb=2222222222222222222,c=3,d=4)
      # to this
      a = dict(aaaaaaaaaaaaaaaaaaaaaaaaa=11111111111111111111,
               bbbbbbbbbbbbbbbbbbbb=2222222222222222222, c=3, d=4)
      # vs to this
      a = dict(aaaaaaaaaaaaaaaaaaaaaaaaa=11111111111111111111,
               bbbbbbbbbbbbbbbbbbbb=2222222222222222222,
               c=3,
               d=4)

  * ``SPLIT_COMPLEX_COMPREHENSION``.  For list comprehensions and generator
    expressions with multiple clauses (e.g multiple "for" calls, "if" filter
    expressions) and which need to be reflowed, split each clause onto its own
    line.

    .. code:: python

      result = [a_var + b_var for a_var in xrange(1000) for b_var in xrange(1000) if a_var % b_var]
      # to this
      result = [
          a_var + b_var for a_var in range(1000) for b_var in range(1000)
          if a_var % b_var
      ]
      # vs to this
      result = [
          a_var + b_var
          for a_var in range(1000)
          for b_var in range(1000)
          if a_var % b_var
      ]

  * ``SPLIT_PENALTY_AFTER_OPENING_BRACKET``.  The penalty for splitting right
    after the opening bracket.

  * ``SPLIT_PENALTY_AFTER_UNARY_OPERATOR``.  The penalty for splitting the line
    after a unary operator.

  * ``SPLIT_PENALTY_ARITHMETIC_OPERATOR``. The penalty of splitting the line
    around the ``+, -, *, /, //, %, and @`` operators.

  * ``SPLIT_PENALTY_BEFORE_IF_EXPR``. The penalty for splitting right before
    an if expression.

  * ``SPLIT_PENALTY_BITWISE_OPERATOR``. The penalty of splitting the line
    around the ``&, |, ^`` operators.

  * ``SPLIT_PENALTY_COMPREHENSION``.  The penalty for splitting a list
    comprehension or generator expression.

  * ``SPLIT_PENALTY_EXCESS_CHARACTER``.  The penalty for characters over the
    column limit.

  * ``SPLIT_PENALTY_FOR_ADDED_LINE_SPLIT``.  The penalty incurred by adding a
    line split to the unwrapped line. The more line splits added the higher the
    penalty.

  * ``SPLIT_PENALTY_IMPORT_NAMES``. The penalty of splitting a list of
    ``from ... import ...`` names.

  * ``SPLIT_PENALTY_LOGICAL_OPERATOR``.  The penalty of splitting the line
    around the ``and`` and ``or`` operators.

  * ``USE_TABS``. Use the Tab character for indentation.


directives
----------
- ``# yapf: disable``
  
  * on a line by itself. disable formatting for the following code.

  * on a line following code. disable formatting for the current line or the
    current expression for multi-line expression.

    .. code:: python

    a = [
        (1, 2, 3),
        (2, 3, 4),
        (3, 4, 5),
    ] # yapf: disable

- ``# yapf: enable`` on a line by itself. (re-)enable formatting for the
  following code.

API
---
- ``yapf.yapflib.yapf_api.FormatCode``

- ``yapf.yapflib.yapf_api.FormatFile``

- parameters:

  * ``style_config``, Either a style name or a path to a file that contains
    formatting style settings. If None is specified, use the default style as
    set in style.DEFAULT_STYLE_FACTORY.

  * ``lines``, A lines argument: A list of tuples of lines ``(start, end)``
    that we want to format. The lines are 1-based indexed.

  * ``print_diff``, bool. Instead of returning the reformatted source, return a
    diff that turns the formatted source into reformatter source.

Noticeable problems
-------------------
- 注意 yapf will format things to coincide with the style guide, but that may
  not equate with readability. 有时 hand-written formatting is better than
  auto-formatting.

- 注意 yapf 不会 modify original source code's token stream, 也就是说, 它不会
  添加或删除任何代码, 只做 reformatting. 这样完全避免 altering the semantics
  of original code. 然而另一方面, 这也让一些代码无法被自动 reformatting. 例如,

  .. code:: python

    # won't be formatted
    FOO = my_variable_1 + my_variable_2 + my_variable_3 + my_variable_4 + my_variable_5 + my_variable_6 + my_variable_7 + my_variable_8
    # will be formatted
    FOO = (my_variable_1 + my_variable_2 + my_variable_3 + my_variable_4 + my_variable_5 + my_variable_6 + my_variable_7 + my_variable_8)
flake8
======
overview
--------
- flake8 is a wrapper around: pyflakes, pycodestyle, McCabe.

installation
------------
- Install flake8 on the correct version of python for your needs.

CLI
---
::

  flake8 [options] [file-or-directory ...]

- Specify files and/or directories you wanna check. Otherwise, all files in
  current directory is processed.
