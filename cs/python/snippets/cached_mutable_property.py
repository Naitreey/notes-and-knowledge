class cached_mutable_property(object):
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.

    Optional ``name`` argument allows you to make cached properties of other
    methods. (e.g.  url = cached_property(get_absolute_url, name='url') )
    """
    def __init__(self, fget, fset=None, fdel=None, name=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = getattr(fget, '__doc__')
        self.name = name or fget.__name__

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        if self.name in instance.__dict__:
            return instance.__dict__[self.name]
        else:
            res = instance.__dict__[self.name] = self.fget(instance)
            return res

    def __set__(self, instance, value):
        if self.fset:
            self.fset(instance, value)
            instance.__dict__[self.name] = value
        else:
            raise AttributeError("read-only attribute")

    def __delete__(self, instance):
        if self.fdel:
            self.fdel(instance)
            del instance.__dict__[self.name]
        else:
            raise AttributeError("can not delete attribute")

    def setter(self, fset):
        self.fset = fset
        return self

    def deleter(self, fdel):
        self.fdel = fdel
        return self
