- ``logging`` module 中, 对于 ``propagate == True`` 的 logger, ``LogRecord`` 在向上层
  传递时, 不会考虑父级 logger 的 level 和 filters, 而是直接传递个父级的各个 handlers.
