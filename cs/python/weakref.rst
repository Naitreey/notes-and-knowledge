overview
========
- Weak reference is a reference to an object that won't keep it from being
  garbage collected. However, until the object is actually destroyed the weak
  reference may return the object even if there are no strong references to it.

- weak reference 是任一种 python interpreter 的 builtin 机制.

- objects that can be weakly referenced:
  class instances, functions written in Python (but not in C),
  instance methods, sets, frozensets, some file objects, generators,
  type objects, sockets, arrays, deques, regular expression pattern objects,
  code objects.

  Several built-in types such as list and dict do not directly support weak
  references but can add support through subclassing.

weak dict
=========
- WeakKeyDictionary. keys are weak.

- WeakValueDictionary. values are weak.

weak set
========

- WeakSet

finalizer
=========
- register a cleanup function to be called when an object is garbage collected.

special attributes
==================

- ``__weakref__``. a cpython implementation detail of weakref. It is a linked
  list storing all weakrefs to the current object. The head of that list (the
  first weak reference to an object) is available via ``__weakref__``. 

  See also: [SOWeakref]_

references
==========

.. [SOWeakref] `What exactly is __weakref__ in Python? <https://stackoverflow.com/questions/36787603/what-exactly-is-weakref-in-python>`_
