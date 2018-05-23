urllib.parse
============

overview
--------
- 提供:
  
  * parsing url to components and back. based on two url syntaxes.

    - ``urlparse()``

    - ``urlsplit()``

    - ``urlunparse()``

    - ``urlunsplit()``


  * parse query string and back.

    - ``parse_qs()``

    - ``parse_qsl()``

    - ``urlencode()``

  * Join components to url (like ``os.path.join()``)

    - ``urljoin()``

    - ``urldefrag()``

  * url quoting (escaping) and unquoting (unescaping)

    - ``quote()``

    - ``quote_plus()``

    - ``quote_from_bytes()``

    - ``unquote()``

    - ``unquote_plus()``

    - ``unquote_to_bytes()``

- 支持两种 url syntax.

  * RFC 1808::

      scheme://netloc/path;parameters?query#fragment

  * RFC 2396::

      scheme://netloc/path;parameters/path;parameters?query#fragment

  两者的区别在于, RFC 2396 中, 每个 url path components 后面都可以添加
  parameters. 这样, parsing result 中就不会存在单独的 parameters 部分.

RFC 1808 syntax url
-------------------

urlparse
^^^^^^^^

- Returns a ``ParseResult`` namedtuple.

- urlparse recognizes a netloc only if it is properly introduced by ‘//’.
  Otherwise the input is presumed to contain only url path and components
  afterwards.

urlunparse
^^^^^^^^^^


RFC 2396 syntax url
-------------------

urlsplit
^^^^^^^^

- similar to urlparse.

- Returns a ``SplitResult`` namedtuple.

urlunsplit
^^^^^^^^^^

query string
------------

parse_qs
^^^^^^^^

- parse query string into a dict. The dictionary keys are the unique query
  variable names and the values are lists of values for each name.

parse_qsl
^^^^^^^^^

- parse query string into a list of key-value pairs. Values of duplicate
  keys are not combined into a list.

urlencode
^^^^^^^^^

- The value element in itself can be a sequence and in that case, if the
  optional parameter doseq is evaluates to True, individual key=value pairs
  separated by '&' are generated for each element of the value sequence for the
  key. The order of parameters in the encoded string will match the order of
  parameter tuples in the sequence.

url quoting/escaping
--------------------

- Taking program data and making it safe for use as URL components by quoting
  special characters and appropriately encoding non-ASCII text. And reverse
  operation.

quote
^^^^^
- By default, this function is intended for quoting the path section of URL.
  The optional ``safe`` parameter specifies additional ASCII characters that
  should not be quoted. It defaults to ``/``.

quote_plus
^^^^^^^^^^
- Also replace spaces by plus signs.

quote_from_bytes
^^^^^^^^^^^^^^^^

unquote
^^^^^^^

unquote_plus
^^^^^^^^^^^^

unquote_to_bytes
^^^^^^^^^^^^^^^^
