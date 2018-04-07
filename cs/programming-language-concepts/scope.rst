- Scope is a set of nested lookup table.

- Compiler construct scope structure during compilation.
  Runtime engine lookups scope structure to resolve lvalues and rvalues.

- lvalue & rvalue.
  
  * lvalue. lvalue resolution aims to find the target variable container in memory.
    It happens during variable assignment.

  * rvalue. rvalue resolution aims to find the target variable's value.

lexical scope
=============
- lexical scope is scope that is defined at lexing time.
  In other words, scope is well-defined at by variable/function/etc. declaration
  statements at author-time.
