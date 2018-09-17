WSGI protocol
=============
overview
--------
- WSGI: web server gateway interface.

- WSGI 是一个 API 级别的调用标准, 它规定了 web server 如何调用 web
  application/framework 以处理请求.

- WSGI 的目的: Provide an implementation-agnostic standard interface between
  web servers and Python web applications or frameworks, to promote web
  application portability across a variety of web servers.
  
  Thus the choice of framework and choice of web server are separated, freeing
  users to choose a pairing that suits them, while freeing framework and server
  developers to focus on their preferred area of specialization.

architecture
------------

server/gateway side
^^^^^^^^^^^^^^^^^^^
* The server side invokes a callable object that is provided by the application
  side.
  
  - 具体这个 callable application object 是如何提供给 server 的, 取决于
    server's implementation.

  - The server or gateway must invoke the application object using positional
    not keyword arguments.

* The application callable is invoked once for each request it receives, which
  returns an iterable yielding the response bytestring.

* The server or gateway must transmit the yielded bytestrings to the client in
  an unbuffered fashion, completing the transmission of each bytestring before
  requesting another one.

* If the iterable returned by the application has a ``close()`` method, the
  server or gateway must call that method upon completion of the current
  request.

application/framework side
^^^^^^^^^^^^^^^^^^^^^^^^^^
* The application is a callable object that accepts two positionals.

  * ``environ``. a dict, see `environ dict`_.

  * ``start_response``. A callable see `start_response callable`_.

  Returns an iterable yielding zero or more bytestrings.

* The same application object must be able to be invoked repeatedly.

middleware
^^^^^^^^^^
* middleware implements the both sides of wsgi interface. It acts as an
  application to its containing server, and as a server to a contained
  application.

* The presence of middleware in general is transparent to both the
  server/gateway side and application/framework side, and should require no
  special support.

environ dict
------------
- envrion contains:

  * CGI environs as defined in IETF CGI specification
    
  * WSGI-required variables

  * server-specific extension variables.  

  * arbitrary OS-specific environmental variables.

- The application is allowed to modify the dictionary in any way it desires.

required CGI variables
^^^^^^^^^^^^^^^^^^^^^^
In general, when any of the following variables is an empty string, it may be
omitted, unless as otherwise noted.

- ``REQUEST_METHOD``. required.

- ``SCRIPT_NAME``. The initial portion of the request URL's "path" that
  corresponds to the application object. This is the application's virtual
  location. can be empty string if it corresponds the root of the server.

- ``PATH_INFO``. The the request url's "path" except for ``SCRIPT_NAME``.  This
  is the url actually considered by application when performing url resolution.

- ``QUERY_STRING``. url's query string. empty if none.

- ``CONTENT_TYPE``. request header value.

- ``CONTENT_LENGTH``. ditto.

- ``SERVER_NAME``. request url's hostname part. required.
  
- ``SERVER_PORT``. ditto for port. required.

- ``SERVER_PROTOCOL``. client request's http protocol version, in form of
  "HTTP/x.x".

- ``HTTP_<variables>``. the client-supplied HTTP request headers prefixed
  with ``HTTP_``. Every request header is converted into this form.

WSGI-required variables
^^^^^^^^^^^^^^^^^^^^^^^
- ``wsgi.version``. a 2-tuple ``(major, minor)``.

- ``wsgi.url_scheme``. url scheme.

- ``wsgi.input``. a file-like object from which to read request body.

- ``wsgi.errors``. a file-like object to which error output can be written.

- ``wsgi.multithread``. true if the application object may be simultaneously
  invoked by another thread in the same process, false otherwise.

- ``wsgi.multiprocess``. ditto for another process.

- ``wsgi.run_once``. true if the server or gateway expects that the application
  will only be invoked once during the life of its containing process.
  Normally, this will only be true for a gateway based on CGI.

server-specific variables
^^^^^^^^^^^^^^^^^^^^^^^^^
- should be named using only lower-case letters, numbers, dots, and
  underscores.
  
- should be prefixed with a name that is unique to the defining server or
  gateway.

start_response callable
-----------------------
- the application must invoke the start_response callable using positional
  arguments

- signature.

  * ``status``. A string in the form ``status_code message`` as in http raw
    response.

  * ``response_headers``. response headers, in form of a list of 2-tuple of
    ``(header_name, header_value)``.

  * ``exc_info=None``. used only when the application has trapped an error and
    is attempting to display an error message to the browser.

  Returns a ``write(body_data)`` callable that takes one positional parameter:
  a bytestring to be written as part of the HTTP response body. This return
  value is for compatibility only and should be avoided if possible.

WSGI implementation examples
----------------------------
* 这些 web server 可能直接作为前端 http 服务器, 或者还需要负载均衡, 或者它们本
  身不是 http server, 还需要前端 http 服务器转译和转发.
  
  例子: gunicorn 等用 python 写的 server, uwsgi 等 C 写的 server (可调用 python
  代码).

uWSGI
=====

uwsgi vs gunicorn
-----------------


Gunicorn
========
