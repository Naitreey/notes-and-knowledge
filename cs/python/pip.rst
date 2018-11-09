overview
========

release and versioning
======================
- *always keep your pip up-to-date*. 不要忽略 pip 关于版本的警告. 否则可能在安
  装时遇到未知问题.

requirements file
=================

syntax
------
::
  [<option>]...
  <requirement specifier> [; markers] [<option>]...
  <archive url/path>
  [-e] <project url/local path>
  -r other-requirements.txt
  -c constraints-file.txt
  # comment
  line \
      continuation

- supported install options:

  * --index-url

  * --extra-index-url

  * --no-index

  * --find-links

  * --no-binary

  * --only-binary

  * --require-hashes

requirement specifier
---------------------
三部分:

- PEP508 format specifier
 
- PEP426 environment markers

- ``--global-option=``, ``--install-option=`` passed to package's
  setup.py.
