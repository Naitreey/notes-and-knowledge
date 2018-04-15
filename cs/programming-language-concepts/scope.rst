- Scope is a set of nested lookup table.

- lvalue & rvalue.
  
  * lvalue. lvalue resolution aims to find the target variable container in memory.
    It happens during variable assignment.

  * rvalue. rvalue resolution aims to find the target variable's value.

lexical scope
=============
- lexical scope is scope that is defined at lexing time.  In other words, scope
  is well-defined by variable/function/etc. declarations at author-time.

- In lexical scoping model, value resolution is performed by traversing the
  nesting of "scopes" in program text.

- Compiler construct scope structure during compilation.  Runtime engine
  lookups scope structure to resolve lvalues and rvalues.

dynamic scope
=============
- In dynamic scoping is defined only at runtime. And it's dynamic, because the
  current scope depends on the current call stack, so it changes as program
  runs.

- value resolution is performed by traversing down stack frames.
