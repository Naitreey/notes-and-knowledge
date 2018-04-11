from collections import OrderedDict


class OrderedDefaultDict(OrderedDict):
    """
    A dict subclass that both preserves key orders and has a default.

    This would have been simply implemented by::

      class OrderedDefaultDict(defaultdict, OrderedDict):
          pass

    except that it doesn't work... because two builtin classes can
    hardly used together in multi-inheritance -- they have incompatible
    struct.
    """

    def __init__(self, factory=None, *args, **kwargs):
        self.default_factory = factory
        super(*args, **kwargs)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value
