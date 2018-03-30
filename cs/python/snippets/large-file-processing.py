#!/usr/bin/env python3

import json
import os
import sys
from collections import defaultdict
from argparse import ArgumentParser


class cached_mutable_property:
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.

    Optional ``name`` argument allows you to make cached properties of other
    methods. (e.g.  url = cached_property(get_absolute_url, name='url') )
    """
    def __init__(self, fget, fset=None, name=None):
        self.fget = fget
        self.fset = fset
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
            raise AttributeError("can not be deleted")

    def setter(self, fset):
        self.fset = fset
        return self

    def deleter(self, fdel):
        self.fdel = fdel
        return self


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("INFILE")
    parser.add_argument("OUTDIR")
    return parser.parse_args()


class EventCache:

    BATCH_SIZE = 5000

    def __init__(self, file):
        self.file = file

    @cached_mutable_property
    def _cache(self):
        return defaultdict(lambda: [])

    @_cache.deleter
    def _cache(self):
        pass

    def aggregate_events(self, to):
        self._ensure_dir(to)
        with open(self.file, "r") as f:
            i = 0
            for line in f:
                if i >= self.BATCH_SIZE:
                    self._flush(to)
                try:
                    event_name, source_id, target_id = line.strip().split()
                except ValueError:
                    continue
                else:
                    self._cache[event_name].append(
                        (event_name, source_id, target_id)
                    )
                    i += 1
            self._flush(to)

    def _flush(self, to):
        for name, events in self._cache.items():
            with open(os.path.join(to, name), "a") as f:
                for e in events:
                    f.write(" ".join(e))
                    f.write("\n")
        del self._cache

    def _ensure_dir(self, dir_):
        os.makedirs(dir_, exist_ok=True)


def main():
    args = parse_args()
    cache = EventCache(file=args.INFILE)
    cache.aggregate_events(to=args.OUTDIR)
    return 0


if __name__ == "__main__":
    sys.exit(main())
