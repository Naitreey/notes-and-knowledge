overview
========

- Sass -- syntactically awesome style sheets.

- Sass is a preprocessor scripting language that is interpreted or compiled
  into Cascading Style Sheets (CSS). 或者也可以看作是一种 CSS 领域的模板语言.

- SassScript is the scripting language itself.

- Sass extends CSS by providing several mechanisms available in more
  traditional programming languages, particularly object-oriented languages,
  but that are not available to CSS3 itself.

language
========

syntax dialects
---------------

- the original indented syntax

  * uses indentation to separate code blocks and newline characters to separate
    rules.
 
  * file extension ``.sass``.

- the newer Sassy CSS (SCSS) syntax

  * uses braces to denote code blocks and semicolons to separate lines within a
    block, just like CSS.

  * file extension ``.scss``.

  * This is now the prefered syntax.

variables
---------
::

  $var: value;

- variables must start with ``$``

- value can be any CSS value.

nesting
-------
::

  selector1 {
    selector2 {
      // rules
    }
  }

module (partial)
----------------
::

  _<module>.scss

- make css modular, without the drawback of ``@import`` directive (which is
  making an separate http request for each imported css file).

- the name of the sass partial files must start with ``_``.

- underscore lets Sass know that the file is only a partial file and that it
  should not be generated into a separate CSS file.

import
------
::

  @import '<module>';

- import scss partial file, where ``module`` is the base name of the partial
  file with leading underscore stripped.

- 注意到 sass 使用与 css 相同的 import directive. 这样相当于是 discourage 
  在 css 中使用 import directive.

mixins
------
::

  @mixin name([$var, ...]) {
    // rules
  }

  @include name(value, ...)

- mixins are just like template function.

- ``@include`` can be used anywhere the expansion of mixin leads to valid CSS
  ruleset.

inheritance
-----------
::

  @extend <selector>;

- inherit/reuse css declarations applied to ``<selector>`` in current
  declaration block.

operators
---------
::

  + - * / %

- scss property value can be an expression, consisting of operators and their
  operands.

- Operands can contain units. In that case, unit conversion is performed
  automatically, with the appropriate unit in resulting value.

implementations
===============
- dart-sass (dart)
 
- ruby-sass (ruby)

- libSass (C++)
 
- js

libSass
-------
- A C++ implementation of Sass interpretation library.

- libSass makes it easier to integrate Sass into more software. Before libSass,
  tightly integrating Sass into a language or software product required
  bundling the entire Ruby interpreter. By contrast, libSass is a statically
  linkable library with zero external dependencies and C-like interface, making
  it easy to wrap Sass directly into other programming languages and tools.

- sassc: A CLI wrapper of libSass
