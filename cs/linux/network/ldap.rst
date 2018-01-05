- implementation: OpenLDAP.

- OpenLDAP 提供了

  * slapd. LDAP server daemon.

  * libldap. written in C. 实现了 LDAP protocol. 可基于 libldap 写客户端或者
    服务端等需要使用 LDAP 的程序.

  * 一系列利用 libldap 实现的 client tools. 例如 ldapsearch, ldapadd, 等操作命令.

  libldap 通过 ``/etc/ldap`` 下的配置文件进行配置. 所有基于 libldap 的程序自动使用.

- 基于 libldap 的 Python bindings 为 python-ldap.
  基于 python-ldap 的 django 认证 backend 为 django-auth-ldap.
