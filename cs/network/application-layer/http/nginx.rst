overview
========

- nginx is:
 
  * HTTP server
   
  * reverse proxy server
   
  * mail proxy server

  * generic TCP/UDP proxy server

  * load balancer

features
--------

HTTP server
~~~~~~~~~~~

- serving static files.
  
- indexing: serving index files, autoindexing.

- open file descriptor cache.

- reverse proxying with caching.

- load balancing and fault tolerance.

- builtin support for FastCGI, uwsgi, SCGI, memcached.

- modular architecture. many filters.

- SSL, TLS SNI support.

- HTTP/2.

- virtual servers.

- keep-alive, pipelined connections support.

- logging, log rotation, syslog.

- URI rewriting.

- conditional processing.

- access control.

- HTTP referer validation.

- file streaming.

- WebDAV.

- response rate limiting.

- simultaneous connection number control.

- IP-based geolocation.

- A/B testing.

- request mirroring.

- nginScript.

mail proxy server
~~~~~~~~~~~~~~~~~

TCP/UDP proxy server
~~~~~~~~~~~~~~~~~~~~

- generic proxying of TCP/UDP.

- SSL, TLS SNI support.

- load balancing, fault tolerance.

- access control.

- conditional processing.

- simultaneous connection number control.

- logging, log rotation, syslog.

- IP-based geolocation.

- A/B testing.

- nginScript.

architecture
------------

- One master and several worker processes. worker processes run under an
  unprivileged user.

- Flexible configuration.

- Reconfiguration and upgrade without interruption of client servicing.

- Support for kqueue (FreeBSD 4.1+), epoll (Linux 2.6+), /dev/poll (Solaris 7
  11/99+), event ports (Solaris 10), select, and poll;

- sendfile.

- File AIO

- DIRECTIO.

- small memory footprint.

master & workder
================

- One master and several worker processes.
  
master
------

- read and evaluate configuration

- maintain worker processes.

worker
------

- Worker processes do actual processing of requests.

- Worker processes run under an unprivileged user.

request processing workflow
===========================
1. 每个 server context 定义一个 virtual server.
   ``listen`` 是该 virtual server 监听的 socket.
   请求由此进入.

   注意一个 ip-port 组合上可以有多个 virtual server. 在物理上, 只需 listen
   一个 socket 即可.

2. 请求的 Host header 与该 ip-port 上的任何 virtual server 的 ``server_name``
   进行匹配.  若任何 virtual server 的 ``server_name`` 都不能匹配, 则使用该
   ip-port 上的 default server.

   default server 是该 ip-port 上第一个 server context 或者是包含
   ``default_server`` 参数的那个.

3. request uri (不包含 query string 部分) 匹配 ``server`` context 中的各个
   ``location`` directives. 选择 match with longest prefix.

- 对于静态文件, 根据 ``root`` directive 作为 root directory. ``root``
  放在 server context 或者 location context 中.

tips
----
- prevent processing requests with undefined server names.

  .. code:: nginx
    server {
        listen      80;
        server_name "";
        return      444;
    }

http core module
================

- ``server_name``. 对于 ``default_server``, 可以指定一个不具有任何意义的
  invalid server_name. 对于 default server, 本身 Host header matching 就
  不起作用.


reverse proxy server
====================

- ``proxy_pass``

uwsgi
=====

- 会设置一些 WSGI protocol 要求的 headers. 包含 HTTP_HOST.

Configuration
=============

- file: ``nginx.conf``

reload configuration
--------------------

Once the master process receives the signal to reload configuration, it
checks the syntax validity of the new configuration file and tries to apply
the configuration provided in it. If this is a success, the master process
opens log files, starts new worker processes and sends messages to old worker
processes, requesting them to shut down. Otherwise, the master process rolls
back the changes and continues to work with the old configuration.

Old worker processes, receiving a command to shut down, stop accepting new
connections and continue to service current requests until all such
requests are serviced. After that, the old worker processes exit.

file structure
--------------

- config file consists of directives.

- simple directives: ``<name> <parameters>;``

- block directives: ``<name> <parameters> {...}``

- context: block directives with directives inside of block.

- main context: config file 里的最外层部分, 即在所有 block context 外部
  的 directives.

- line comment: ``#``

logging
=======

log rotation
------------
- 手动重命名日志文件.

- send SIGUSR1 to master.

这两步可通过 logrotate 自动执行.

The master process will then re-open all currently open log files and assign
them an unprivileged user under which the worker processes are running, as an
owner. After successful re-opening, the master process closes all open files
and sends the message to worker process to ask them to re-open files. Worker
processes also open new files and close old files right away.

Command line
============

signal
------

- ``nginx -s <signal>`` 给 master process 发信号. 通过读取 ``pid`` directive
  指向的文件获取 master pid.

signals to master
~~~~~~~~~~~~~~~~~
  
- stop. SIGTERM, SIGINT. shutdown quickly.
 
- quit. SIGQUIT. stop with waiting for work processes to finish
  serving current requests.
 
- reload. SIGHUP. reload configuration.
  
- reopen. SIGUSR1. reopen log files.

- SIGUSR2. upgrading nginx executable.

- SIGWINCH. graceful shutdown of worker processes.

signals to worker
~~~~~~~~~~~~~~~~~

- SIGTERM, SIGINT. fast shutdown.

- SIGQUIT. graceful shutdown.

- SIGUSR1. re-open log files.

- SIGWINCH. abnormal termination for debugging.

upgrade on the fly
==================
- see https://nginx.org/en/docs/control.html
