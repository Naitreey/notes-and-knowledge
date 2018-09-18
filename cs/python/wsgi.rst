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

  Returns an iterable yielding zero or more bytestrings corresponding to
  response body.

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

- ``wsgi.file_wrapper``. server/gateway may expose high-performance file
  transmission facilities (possibly provided by OS) via this key. An
  application may use this "file wrapper" to convert a file or file-like object
  into an iterable that it then returns as result.

  The file wrapper callable has the following signature:

  * ``filelike``. the file-like object to be sent. required.

  * ``block``. block size suggestion. optional.

  The callable must return an iterable object, and must not perform any data
  transmission until and unless the server/gateway actually receives the
  iterable as a return value from the application.

server-specific variables
^^^^^^^^^^^^^^^^^^^^^^^^^
- should be named using only lower-case letters, numbers, dots, and
  underscores.
  
- should be prefixed with a name that is unique to the defining server or
  gateway.

start_response callable
-----------------------
- The ``start_response()`` callable is used to begin the HTTP response.

- the application must invoke the start_response callable using positional
  arguments.

signature
^^^^^^^^^

* ``status``. A string in the form ``status_code message`` as in http raw
  response.

* ``response_headers``. response headers, in form of a ``list`` of 2-tuple of
  ``(header_name, header_value)``. The server may change the list in any way
  it desires.

  - If the application omits a header required by HTTP (or other relevant
    specifications that are in effect), the server or gateway must add it.

  - ``start_response`` must not actually transmit the response headers.
    Instead, it must store them for the server or gateway to transmit only
    after the first iteration of the application return value.
  
    This delaying of response header transmission is to ensure that buffered
    and asynchronous applications can replace their originally intended output
    with error output, up until the last possible moment.

* ``exc_info=None``. A ``sys.exec_info()`` tuple. used only when the
  application has trapped an error and is attempting to display an error
  message to the browser.

  - This argument should be supplied by the application only if
    ``start_response`` is being called by an error handler.

  - The application must not trap any exceptions raised by ``start_response``,
    if it called ``start_response`` with ``exc_info``.

  - The application may call ``start_response`` more than once, if and only if
    the ``exc_info`` argument is provided.
  
* Returns a ``write(body_data)`` callable that takes one positional parameter:
  a bytestring to be written as part of the HTTP response body. This return
  value is for compatibility only and should be avoided if possible.

Handling Content-Length of response
-----------------------------------
- If the application supplies a ``Content-Length`` header, the server should
  not transmit more bytes to the client than the header allows, and should stop
  iterating over the response when enough data has been sent

Handling unicode
----------------
- HTTP does not directly support Unicode, neither does WSGI. all strings passed
  to or from the server must consist of ISO-8859-1 characters.

Handling error
--------------
- applications should try to trap their own, internal errors, and display a
  helpful message in the browser. 

- If no output has been written when an exception occurs, the call to
  ``start_response`` will return normally, and the application will return an
  error body to be sent to the browser.
  
- If any output has already been sent to the browser, ``start_response`` will
  reraise the provided exception.  This exception should not be trapped by the
  application, and so the application will abort. The server or gateway can
  then trap this (fatal) exception and abort the response.

- Servers should trap and log any exception that aborts an application or the
  iteration of its return value. If a partial response has already been written
  to the browser when an application error occurs, the server or gateway may
  attempt to add an error message to the output, if the already-sent headers
  indicate a ``text/*`` content type that the server knows how to modify
  cleanly.

WSGI implementation examples
----------------------------

server/gateway side
^^^^^^^^^^^^^^^^^^^
- 作为被调用的脚本, e.g., apache CGI script. (这是设计使用环境变量传递来输入的
  原因.)

- 直接作为前端 http 服务器. e.g., gunicorn.
 
- 配合 load balancer. e.g., bottle.py + haproxy.
 
- 本身不是 http server, 还需要前端 http 服务器转译和转发. e.g., uwsgi.

- C 写的, embed cpython interpreter, 加载 python web application/framework.
  e.g., uwsgi.
  
uWSGI
=====

uwsgi vs gunicorn
-----------------


Gunicorn
========
