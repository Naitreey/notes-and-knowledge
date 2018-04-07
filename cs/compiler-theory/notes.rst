steps:

- tokenization/lexing. breaking up a string of characters into meaningful
  chunks, called tokens. 

  The difference of tokenization and lexing is between stateless and stateful
  way of doing things.  If the tokenizer were to invoke stateful parsing rules
  to figure out whether a should be considered a distinct token or just part of
  another token, that would be lexing.

- Parsing. taking a stream (array) of tokens and turning it into a tree of
  nested elements, which collectively represent the grammatical structure of
  the program. This tree is called an "AST" (Abstract Syntax Tree).

- Code generation. the process of taking an AST and turning it into executable
  code.
