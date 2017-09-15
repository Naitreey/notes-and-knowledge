- ``salt <target> <module>.<function> [args]...``

- 使用 ``sys.doc`` module 获取 module/function doc.

- target selection (``man salt(1)``).

  * minion id.

  * shell globbing.

  * PCRE regex.

  * Grain system with glob.

  * Grain system with PCRE.

  * target list.

  * all above combined.

- Grains.

  * The static information SaltStack collects about the underlying managed system.

  * Add custom ``role`` grain to minion configuration file to categorize minions
    by functionality.
