security
========
email header injection exploit
------------------------------
- MIME can deal with multiple headers of the same name.

- User can inject additional headers with newline when inputing email headers. 因此
  若不对输入进行过滤, 用户可以操纵任意 header 的值 (例如输入 To, From header 时).

- To protect against header inject exploit, 若用户输入的 header 中包含 ``\n``, ``\r``
  等换行符, 则进行过滤或报错.

- See also [EmailHeaderInjection]_.

references
==========
.. [EmailHeaderInjection] `Email Header Injection Exploit <http://nyphp.org/phundamentals/8_Preventing-Email-Header-Injection>`_
