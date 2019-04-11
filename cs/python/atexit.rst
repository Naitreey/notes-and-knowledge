overview
========
- 类似 ``atexit(3)``, to register and unregister cleanup functions that are
  called at *normal* interpreter exit (``sys.exit``).

- Execution order: atexit runs registered functions in the reverse order in
  which they are registered. 这是因为 the assumption is that lower level
  modules will normally be imported before higher level modules and thus must
  be cleaned up later.

- *The functions registered via this module are not called when the program is
  killed by a signal not handled by Python, when a Python fatal internal error
  is detected, or when ``os._exit()`` is called.*

- If an exception is raised during execution of the exit handlers, a traceback
  is printed (unless SystemExit is raised) and the exception information is
  saved. After all exit handlers have had a chance to run the last exception to
  be raised is re-raised.

module level functions
======================
- ``register(func, *args, **kwargs)``. register func to be called with args and
  kwargs at normal interpreter exit. This function returns func, which makes it
  possible to use it as a decorator.

- ``unregister(func)``. remove func from the list of functions to be called at
  interpreter shutdown. func is guaranteed not to be called when the
  interpreter shuts down, even if it was registered more than once. It silently
  does nothing if func was not previously registered.
