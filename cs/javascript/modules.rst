overview
========
- module pattern. Using function and closure to emulate lousy module/class
  interface. Basic concepts:

  * An outer enclosing function, which acts as a module or class container.
    
  * The function itself can be viewed as constructor.
    And the function's parameters are module/class's constructor parameters.

  * attributes and methods are defined in the function.

  * When called, the outer function must return a public API instance of the
    module/class, which can be a plain object instance or an inner function
    instance.

  * All identifiers in outer function's scope that are not part of the public
    API, are module/class's private members.

Universal Module Definition (UMD)
=================================
