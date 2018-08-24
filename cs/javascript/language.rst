overview
========
- JavaScript, abbreviated JS.

- interpreted language. V8 implementation has JIT engine, JS code is
  pre-compiled to machine code then executed.

- weakly typed. type coercion may happen implicitly (WTFJS_).

- JS 与 C/Python/Java 的一大区别是, JS 强调 async 概念. 异步思想和
  编程范式深深嵌入 JS 的整个语言. 可以说, JS 最独特的思想就是单线程
  异步并发思想. JavaScript has a concurrency model based on an
  "event loop". 常用的很多 builtin function 等都是异步的. JS engine
  has builtin event loop.

definitions
===========

- host object: object supplied by the host environment. e.g.,
  window, document, XMLHttpRequest, etc.

  Host objects are not defined by spec. They are implemented and provided by
  host environment, which is browser, nodejs interpreter, etc. These objects
  are implemented as builtin part of host environment. So they may be
  implemented in C/C++, and just a js wrapper.

lexical grammer
===============

comment
-------
support both types of C comment syntaxes:

- single-line: ``//``

- multi-line: ``/* */``. Can appear anywhere on a line.

identifier
----------
If we consider only ASCII chars, identifier must consists of
a-z, A-Z, 0-9, $, or _. And it must not starts with number.

data types
==========

- 7 builtin types. null, undefined, string, number,
  boolean, symbol, object.

  All types except object are primitives.

- value-copy vs reference. On assignment, 到底是复制 value 还是复制 reference
  完全取决于 value 的类型. Values of primitive types are always copied on
  assignment; instances of object type are referenced to the same object on
  assignment.

- values of primitive types are immutable, i.e., primitive values can not be
  modified inplace. modifying their values automatically generates a new value.

- Unlike python, object is just one of the basic builtin types.  In other
  words, string, number, etc. are all distinct types as basic as object type.
  object is not base type of *all* types (WTFJS_).

  Therefore, string, number, etc. does not have hash-map-like
  functionality.

- Majority of data types have a corresponding function that have
  two purpose:

  * as type constructor.

  * as type conversion function.

- autoboxing (WTFJS_). Under certain conditions, primitive value
  will be automatically wrapped in its object equivalent. These includes
  [SOJSAutobox]_

  * When accessing a primitive value's property.

  * When passed as ``this`` binding target.

undefined
---------

- ``undefined`` is the only value of Undefined type.

Some cases when undefined is resultant:

- an undefined variable's type is ``"undefined"`` (WTFJS_). But it results in
  ``ReferenceError`` if used directly.

- an declared variable's default value is ``undefined``.

- A function returns ``undefined`` if nothing is returned explicitly via
  ``return`` statement.

- ``undefined`` is not a reserved keyword, but an identifier. 准确地讲,
  undefined is a readonly property of global object (WTFJS_). 由于 undefined
  is not reserved, it's technically possible to define a local variable
  named ``undefined``.

null
----
- ``null`` is the only value of Null type.

- It is a bug in JS language definition that: ``typeof null === "object"``.

boolean
-------

string
------

- 由于 autoboxing, 这里只记录 string literal formats. 关于方法和其他机制,
  see `String`_.

- strings are immutable. 对 string 的任何 inplace modification 都不会
  生效. 凡是涉及到 property modification, 修改的是 autobox 后的对像上的
  属性, 并没有改变原 string primitive.


string literal
^^^^^^^^^^^^^^
- a sequence of unicode characters surrounded by single or double quotes.

- A string literal must be on one physical line.

- 常见的 backslash escaped sequence 可以加入 string literal 中.

  * 支持 unicode escape sequence: ``\uXXXX`` 以及 ``\u{X}...\u{XXXXXX}``.

  * newline at the end of physical lines can be escaped, thus spanning
    string literal across multiple physical lines. 生成的 string literal
    不包含 escaped ``\n``.

template literal
^^^^^^^^^^^^^^^^
::

  [tag]`string ${expression}`

- a type of string literal that allows embedded expressions.

- surrounded by backtick ``\```. to escape backtick char in template literal,
  use backslash escape ``\\\```.

- template literal can be multiline, line breaks are preserved as ``\n`` in
  resulting string.

- placeholder.

  * format::

      ${expression}

  * 任何 expression, 只要 evaluate 至一个值, 就可以放在里面. 甚至可以包含
    nested template literal.

- nested template literal. 由于 placeholder 里面可以是任何 expression, it can
  also be template literal expression. 里面的 backtick 无需 escape.::

    const classes = `header ${ isLargeScreen() ? '' :
     `icon-${item.isCollapsed ? 'expander' : 'collapser'}` }`;

- tag function.

  - 整个 template literal 被分成以下两个部分

    * 一个字符串数组, 包含除了 placeholders 之外的各个 string segements.

    * a sequence of placeholder expressions' values.

    这两部分作为参数传入 tag function, 注意第二部分是作为 vararg positional 参数
    传入的. 由 tag function 决定最终输出值是什么, 甚至可以不是字符串.

  - string segment 数组包含一个特殊属性: ``.raw``, 其值为各个 string segments
    的 raw form, 即 input form. 相当于 python raw string.

  - 默认的 tag function 直接将输入参数 concatenated 构成输出.

  - tag function examples:

    * ``String.raw()``: make template literal like those raw strings in python::

        String.raw`\d+\nwhatever\\` // output: '\\d+\\nwhatever\\\\'

- ``tag`string``` 形式可以看作是对 C 和 python, SQL 等语言里面的 prefix string
    的一般化.

symbol
------
::

  Symbol([value])

- The Symbol data type's sole purpose is to used as identifier for speical
  object properties. Their intended use is to avoid name clashes with existing
  properties.

- Symbol function creates a new symbol, every created symbol is unique.::

    Symbol(1) !== Symbol(1)

- Symbol function is not class constructor, cannot be called with new operator.
  无论 Symbol 的用法, 以及 symbol instance 的属性跟 Object.prototype 有多像,
  Symbol 不是 Object (WTFJS_).

- Use ``Object(symbol)`` to create a symbol's object wrapper form.

- Symbols are intended for special properties, 无论 symbol property 是否 enumerable,
  for...in loop 都不会包含这些属性.

static methods
^^^^^^^^^^^^^^

- ``for(key)``. get or create a symbol for key in gobal symbol registry.

- ``keyFor(sym)``. get symbol key of global symbol sym.

methods
^^^^^^^
- ``toString()``. format::

    Symbol(<key>)

- ``valueOf()``. return symbol itself.

Well-known symobls
^^^^^^^^^^^^^^^^^^

Symbol.iterator
""""""""""""""""

Symbol.species
""""""""""""""

- @@species is a readonly accessor property that returns a constructor function
  (class function). The returned constructor function is used to create derived
  objects from this class's instances.

- A derived object is one created after  a specific operation on the original
  object.

  For example, ``Array.prototpye.map()`` creates a derived array as the result
  of map operation. It actually consults @@species accessor property to know
  what class to use as the result.

  Example::

    class SomeArray extends Array {
        get [Symbol.species] {
            return Array;
        }

        some_method() {
            //
        }
    }

  See also: [WellKnownSymbols]_.

Symbol.toPrimitive
""""""""""""""""""

Symbol.toStringTag
""""""""""""""""""

Symbol.match
""""""""""""

Symbol.replace
""""""""""""""

Symbol.search
""""""""""""""

Symbol.split
""""""""""""

Symbol.hasInstance
""""""""""""""""""

Symbol.isConcatSpreadable
""""""""""""""""""""""""""

Symbol.unscopables
""""""""""""""""""

number
------
- literal forms::

    // decimal forms
    NN[.[NN]]
    [0].NN
    // exponential forms
    NN{e|E}NN
    // octal, hex, binary integer forms
    0{o|O}NN
    0{x|X}NN
    0{b|B}NN

  注意由于 ``NN.`` 是合法的 number syntax, digits 后面的第一个 ``.``
  会认为是 decimal point, 而不是 attribute reference. 例如::

    1.toFixed // SyntaxError
    (1).toFixed // OK
    1..toFixed // OK
    1.1.toFixed // Ok

- JS number type 类型值全部是 floating-point number. 没有真正的 integer.

  * 整数完全依靠 53 个 significand bits 来保证准确. 这导致,
    ``Number.MAX_SAFE_INTEGER`` 以及 ``Number.MIN_SAFE_INTEGER`` 之外的
    64bit 整数不能使用 number type 存储 (WTFJS_). 目前需要使用 ``node-int64``
    package.  bigint feature 可能在 ESnext 中包含.

- JS number type implements IEEE 754 double precision number.

- Very large or very small numbers will by default be outputted in exponent
  form.

- normal zero and negative zero. An requirement of IEEE 754.

  * 0 and -0 always compares equal.

  * multiplication, division can lead to -0.

  * addition, substraction can not lead to -0.

  * ``-0``'s string form is ``"0"``

  * However, the reverse is not true. ``"-0"`` to number leads to ``-0``.

object
------

- constructor function: ``Object()``

- literal form: ``{...}``.

  * in literal form, property name must be a string, string can be specified
    without quotes, if it's a valid identifier. 注意 property name 不能是
    expression (Unlike python), 除非使用以下 ``[expression]`` 形式.

  * computed property names: an expression, surrounded by a ``[ ]`` pair, in
    the key-name position of an object-literal declaration.::

      let x = {
          [{"s": 1}]: 2,
          [true]: 3,
          [Symbol.Something]: "sef"
      };

  * concise method definitions: functions defined in object literal form, 可
    省去 function keyword, 形成如下形式::

      let x = {
          // function
          f() {},
          // generator
          *g() {},
          // async
          async h() {},
          // with computed property name,
          ["f" + "g"]() {},
      }

    注意 normal function, generator function, async function, etc, 以及配合
    computed property name 的各种形式都可以使用.

    注意, concise method definition 定义的函数, 是 anonymous function
    expression, 等价于::

      f: function () {}

    具有 anonymous function 的一切问题.

  * concise accessor property definitions. Accessor properties can be defined
    using ``get``, ``set`` keyword in object literal form. Rather than having
    to use ``Object.defineProperty``.::

      let x = {
          get prop() {
              //
          }
          set prop(value) {
              //
          }
      }

- constructor: ``Object()``.

- an object is simply a hash map. In JS, virtually every non-primitive instance
  is a object. No matter what constructor it is created with.

object property
^^^^^^^^^^^^^^^

- object property names can only be string. If non-string values are specified
  as attribute keys, they will firstly be coerced to string.

- property access:

  * ``.``. for keys that are valid identifiers.

  * ``[]``. for keys that are any strings.

- property descriptor. In JS, a object property 本质上是由 property name
  string + property descriptor 组成的. property value 只是 property descriptor
  的 ``value`` 部分.

  这种对 property 的封装, 给 property 赋予了 value 之外的各种性质. 这有些类似
  python 中的 property 或者更一般化的 descriptor protocol.

- property's attributes.

  * value (default: undefined).

  * writable (default: false). true if the property's value may be changed. If
    a property's value is not writable, in non-strict mode, assignment to it
    will be silently ignored; in strict mode, a TypeError will be raised.

    ``writable: false`` 等价于设置一个 raise TypeError 的 setter.

  * configurable (default: false). true if the property descriptor itself can
    be modified.  In other words, the property name as a variable can change
    its value (being assigned another property descriptor), and can be deleted.

    If a property is not configurable, it cannot be re-defined using a
    different definition, which will raise TypeError. But re-define it
    changing only value is ok. In non-strict mode, deleting a
    non-configurable property will be silently ignored; in strict mode,
    TypeError will be raised.

  * enumerable (default: false). true if the property shows up during iteration
    of object property.

    A non-enumerable property does not show up in object's representation.

  * get (default: undefined). For access descriptor, getter is called to get
    the property value.  Property getter can be defined via
    ``defineProperty()`` or using ``get`` keyword in object literal
    declaration::

      var x = {
          _a: 1,
          get a() {
              return this._a;
          },
          set a(value) {
              this._a = value;
          }
      }

  * set (default: undefined). ditto. If setter is not defined for a property,
    in non-strict mode, property assignment will be ignored; in strict mode,
    TypeError is raised.

  当使用 property assignment 形式创建 property, 生成的 property descriptor 的
  writable, enumerable, configurable 都是 true. Use ``Object.defineProperty()``
  to explicitly define property descriptor's attributes.

- property descriptor 的分类:

  * data property descriptor.

  * accessor property descriptor. has ``get`` and/or ``set`` attributes.
    Accessor property descriptor cannot define ``writable`` or ``value``
    attributes.

- property immutability.

  * constant property. Whether a property is writable.

  * extensiblitiy. An object is extensible if new properties can be added to
    it. If an object is not extensible, in non-strict mode, further property
    addition operation will be silently ignored; in strict mode, TypeError will
    be raised.

  * seal. An object is sealed if it is not extensible and if all its properties
    are non-configurable. In non-strict mode, further property addition or
    configuration will be silently ignored; in strict mode, TypeError will be
    raised.

  * freeze. Seal an object and make all data property non-writable.

object prototype
^^^^^^^^^^^^^^^^
- ``prototype`` property object 是 JS 中类和继承的实现基础. See `class`_.

constructor
^^^^^^^^^^^
::

  Object([value])
  new Object([value])

- 无论有没有 new, 效果都是根据 ``value`` 生成一个 object wrapper. 当没有 new
  时, 可以理解为转换成 object wrapper 形式, 但其实是一个意思.

- When ``value`` is null or undefined, return an empty object.

  When ``value`` is other primitive value, return its corresponding object
  wrapper form.

  When ``value`` is already an object, return ``value`` unchanged.

static methods
^^^^^^^^^^^^^^

prototype related
""""""""""""""""""
- ``create(proto[, propertiesObject])``. Create a new object using ``proto``
  as its prototype (i.e., its class). The created object is linked to ``proto``.

  If ``proto === null``, the created object has an empty prototype chain. It's
  not linked to anything including Object.prototype. The created object has
  only own properties. It is useful for purely storing data as properties.

  ``propertiesObject`` is an object whose enumerable own properties are property
  descriptor definitions to be added to the created object. 也就是说该 object
  符合 ``Object.defineProperties()`` 参数形式.

- ``getPrototypeOf(obj)``. returns the prototype of the obj. Note it might be
  null.

- ``setPrototypeOf(obj, prototype)``. Set ``[[Prototype]]`` of ``obj`` to be
  ``prototype``.

  * 注意修改一个对象的 prototype chain 会影响所有相关代码的优化和执行效率. 该
    操作可能对效率产生巨大的负面影响. avoid setting the ``[[Prototype]]`` of an
    object. Instead, create a new object with the desired ``[[Prototype]]`` using
    ``Object.create()``.

property manipulation
"""""""""""""""""""""
- ``getOwnPropertyDescriptor(obj, prop)``. Returns a own property's property
  descriptor.

- ``getOwnPropertyNames(obj)``. returns an array of all own properties including
  non-enumerable properties. This does not include property names as Symbols.

- ``getOwnPropertySymbols(obj)``. An array of all property symbols found
  directly upon the given object.

- ``defineProperty(obj, prop, descriptor)``. ``descriptor`` object is used to
  set property descriptor's attributes, 它并不是直接成为了 descriptor. 定义时,
  ``descriptor`` 中未指定的 attributes 使用原有的值或默认值.

  ``descriptor`` 部分是提供 property descriptor 的配置, 若原 property 不存在则
  新建一个. 根据提供的配置项, 这可以是只修改 property 的值, 或者修改 property
  的属性 (writable, configurable, enumerable 等), 或者将 data property descriptor
  改成 accessor property descriptor 等等.

- ``preventExtensions(obj)``. prevents new properties from ever being added to
  an object.

- ``isExtensible(obj)``.

- ``seal(obj)``. Seal an object, preventing new properties from being added to
  it and marking all existing properties as non-configurable.

- ``isSealed(obj)``.

- ``freeze(obj)``.

- ``isFrozen(obj)``.

- ``assign(target, ...sources)``. shallow copy source objects into target object.
  Return target object.

  * only copies enumerable and own properties from a source object to a target object.

  * It uses ``[[Get]]`` on the source and ``[[Set]]`` on the target, so it will
    invoke getters and setters.

iteration
"""""""""
- ``keys(obj)``. returns an array of object's enumerable property names, in the
  same order as for...in loop would.

- ``values(obj)``. return an array of object's own enumerable property values,
  in the same order as for...in loop wound.

- ``entries(obj)``. returns an array of a given object's own enumerable
  property ``[key, value]`` pairs.

equality and sameness
""""""""""""""""""""""

- ``is(value1, value2)``. test two values based on same-value equality. Here,
  same-value means values are functionally identical in all contexts.

  这只对 -0 和 NaN 相关的判断有意义. 除此之外, 与 ``===`` 的效果相同, 但可能
  执行效率比 ``===`` 慢很多.::

    Object.is(-0, 0) // false
    Object.is(Number.NaN, Number.NaN) // true

instance properties
^^^^^^^^^^^^^^^^^^^
defined in ``Object.prototype``.

class and prototype
""""""""""""""""""""
- ``constructor``. A reference to the function that created this object.

  * All objects have a consturctor, except for ``Object.create(null)``.

  * Objects created without the explicit use of a constructor function (i.e.
    the object and array literals) will have a constructor property that points
    to the Fundamental Object constructor type for that object.

  * The attribute is writable. So it's not entirely reliable. 例如, 如果
    prototype 属性完全由另一个 object 替换, 则不能保证其值可信.

- ``isPrototypeOf(obj)``. test whether the object appears in obj's prototype
  chain. 与 instanceof operator 进行的是类似的判断.

property manipulation
"""""""""""""""""""""

- ``hasOwnProperty(<prop>)``. Whether the object has this own property.

- ``propertyIsEnumerable(<prop>)``. Whether the property is enumerable.

conversion
""""""""""
以下方法用于各种 abstract operation 中的转换流程中.

- ``toString()``. Return string representation of object. The default
  implementation returns ``[object <type>]``, where ``type`` is one of
  native object types. 注意不是 class function.::

    > Object.prototype.toString.call(null)
    '[object Null]'
    > Object.prototype.toString.call(1)
    '[object Number]'
    > Object.prototype.toString.call(undefined)
    '[object Undefined]'
    > Object.prototype.toString.call(true)
    '[object Boolean]'
    > Object.prototype.toString.call(Symbol.iterator)
    '[object Symbol]'
    > Object.prototype.toString.call("")
    '[object String]'
    > Object.prototype.toString.call({})
    '[object Object]'

- ``valueOf()``. Return the primitive value of object. Default implementation
  returns the object itself. 所以实在没啥用. 所有子类都有 override 这个方法.::

    > Object.prototype.valueOf.call("")
    [String: '']
    > Object.prototype.valueOf.call(1)
    [Number: 1]
    > Object.prototype.valueOf.call({})
    {}

[[Class]]
---------
- objects have an internal ``[[Class]]`` property, 其值是 built-in native
  constructor that's related to the value.

object subtypes
---------------

- built-in subtypes of object: String, Number, Boolean, Array, Function, Date,
  RegExp, Error.

- built-in object types' constructors, including: Object, String, Number,
  Boolean, Array, Function, Date, RegExp, Error, can all be called with or
  without ``new`` operator.

  * 对于 String, Number, Boolean, 没有 ``new`` operator, 只是作为 function call
    时, 是作为转换函数;

  * 对于 Object, Array, Function, RegExp, Error, 有没有 new operator, 效果都一样.

  * 对于 Date, 没有 new 返回当前时间字符串.

- 对于 Object, String, Number, Boolean, Array, Function, RegExp, Error, 它们的
  ``.prototype`` 属性是该类型的一个基本模型, 对应于该类型的 default value. 但是
  注意 instanceof check 不会认为它们是相应类型的实例, 因为 prototype chain 的关系.

String
------
::

  String([arg])
  new String([arg])

- String is string primitive type's object counterpart.

- 若 ``arg`` omitted, return "" empty string; 否则根据 `ToString`_
  转换成字符串. 当不使用 ``new`` operator 时, ``String(arg)`` 就是在
  进行 explicit type conversion.

- When ``String`` function is used not as a constructor, it's a convertion
  function, which converts its input to string primitive value.

- String instances are iterable objects, i.e., String implements the
  @@iterator method.

- String instsances are array-like objects. String objects have length
  property, and have sensible numerical index properties which returns
  individual characters.

- String instance 的 numerical index properties 以及其他重要 properties 都是
  ``writable: false, configurable: false``. 这对应于 string primitive
  is immutable.

  但注意 String instance is extensible.

- String encoding. JS 字符串 API 不完整支持 unicode character.

  JS string 使用 UTF-16 encoding 存储 (WTFJS_). 并且奇葩的 是, 它认为每个 16bit
  code unit 是一个字符, 而不是一个完整的 unicode point 是一个字符. 对于 BMP
  之内的字符, 这没有问题, 但对于 BMP 之外的字符, 一个 字符以多个 code unit
  编码保存. 这样 ``charAt``, indexing 等给出的是 code unit 位置的内容,
  而不一定是预期字符. 例如::

    '𝌆'.length === 2

  为了得到字符串中第 i 个 unicode character 的可靠方式只有两种:

  * String 的 @@iterator 能够保证按照 unicode point 对字符进行遍历. 因此::

      [...string][i]

  * code point methods::

      String.fromCharPoint(string.codePointAt(i))

constructor
^^^^^^^^^^^
- as normal function, convert input to string primitive representation,
  calling `ToString`_.

- as constructor, create String object with that string representation value.

static methods
^^^^^^^^^^^^^^

- ``fromCharCode(num1, num2, ...)``. from utf-16 code unit.

- ``fromCodePoint(num1, num2, ...)``. class method that build a string
  from unicode points.

- ``raw(strings, ...substitutions)``. used for template literal tag function.
  Return raw string like python raw string.

attributes
^^^^^^^^^^

- length.

- <N>. note that indexes are attributes. 注意给出的是 utf-16 code unit 位置的值.

methods
^^^^^^^

character
"""""""""

- ``charAt(n)``. Note it counts utf-16 code unit.

- ``charCodeAt(n)``. Note it counts utf-16 code unit.

- ``codePointAt(n)``. Note it counts unicode point.

substring
""""""""""
- ``includes(substr[, position])``. test substring in string.

- ``indexOf(substr[, position])``. first occurrence.

- ``lastIndexOf(substr[, position])``. last occurrence.

- ``startsWith(substr[, position])``.

- ``endsWith(substr[, position])``.

- ``match(regexp)``.

- ``search(regexp)``.

slice
""""""
- ``slice([begin[, end]])``.

- ``substr(start[, length])``. slice from start through length chars. (WTFJS_)

- ``substring()``. useless. (WTFJS_)

manipulation
""""""""""""
- ``concat(str1, str2, ...)``. concatenate string with the argument strings.
  Why not use addition operator?

- ``replace(regexp|substr, replacement|function)``. returns a new string with
  replacements.

  * With ``regexp``, use ``g`` flag to perform a global search and replace.

  * When using ``substr``, it is treated as a verbatim string, and only the
    first occurrence will be replaced.

  * In ``replacement`` string, the following ``$``-patterns are recognized:

    - ``$$`` literal $.

    - ``$&`` the entire matched substring.

    - ``$n`` nth (1-based) submatch group.

    - ``$``` the portion of the string that precedes the matched substring.

    - ``$'`` the portion of the string that follows the matched substring.

  * For ``function``, its return value is used as replacement string.
    its arguments are as follows:

    - ``match``. the entire matched substring.

    - ``p1``, ``p2``, ... nth submatch group.

    - ``offset``. offset of matched substring relative to the entire string.

    - ``string``. the entire string being examined.

- ``split([separator[, limit]])``

- ``trim()``. removes whitespace from both ends of a string, return the new
  string.

- ``trimStart()``, ``trimLeft()``. those are aliases (WTFJS_).

- ``trimEnd()``, ``trimRight()``.

letter case
"""""""""""
- ``toLowerCase()``

- ``toUpperCase()``

- ``toLocaleLowerCase()``

- ``toLocaleUpperCase()``

conversion
""""""""""
- ``toString()``. Return string representation of the object. For String, just
  return primitive string equivalent. The same as valueOf.

- ``valueOf()``. return primitive string value of String object.

formatting
""""""""""
- ``padStart(target_length[, padstr])``.

- ``padEnd(target_length[, padstr])``.

- ``repeat(count)``.

iteration
""""""""""
- ``[Symbol.iterator]()``. iterating chars of string.

misc
""""
- ``localeCompare()``

- ``normalize()``

Number
------

- number primitive type's object counterpart.

- constructor function: ``Number()``.

constructor
^^^^^^^^^^^
::

  new Number([value])
  Number([ value ])

- If value is omitted, default to 0.

- Performing `ToNumber`_ conversion before creating Number instance.

- If not with ``new``, only do type conversion and return a number primitive.

static attributes
^^^^^^^^^^^^^^^^^

- ``EPSILON``. The smallest interval between two representable numbers. 标准
  高等数学术语.

- ``MAX_SAFE_INTEGER``.

- ``MIN_SAFE_INTEGER``.

- ``MIN_VALUE``. the smallest positive number.

- ``NaN``. Not a Number. Representing a invalid number resulted from failed
  numerical operations.

  * By definition, NaN is the only number that does not equal to itself.
    因此, 不能使用 ``a == NaN`` 进行判断. 需要使用 ``Number.isNaN`` 进行判断.

- ``POSITIVE_INFINITY``.

- ``NEGATIVE_INFINITY``.

static methods
^^^^^^^^^^^^^^

- ``isNaN(value)``.

- ``isFinite(value)``

- ``isInteger(value)``. 即使是在 MAX_SAFE_INTEGER 和 MIN_SAFE_INTEGER 之外的整数
  也 return true.

- ``isSafeInteger(value)``

- ``parseFloat(string)``. 与 ``Number()`` constructor 不同, 并没有使用 `ToNumber`_
  operation. 因此不提供与之完全相同的对各类型的转换逻辑. 这里, 主要用于转换字符串.
  允许 leading whitespace chars, 和 any trailing unrecognized chars. it returns
  the value up to a valid number and ignores all remaining text. 对于不识别的字符串
  给出 NaN.

- ``parseInt(string[, radix])``. ditto for integer only.

methods
^^^^^^^

- ``toExponential([fraction_digits])``. default use as many number of digits as
  needed after decimal point.

- ``toFixed([fraction_digits])``. To fixed point representation, number of
  digits after decimal point defaults to 0.

- ``toPrecision([precision])``. in fixed-point or exponential notation rounded
  to precision significant digits.

- ``toString([radix])``. return string form in the specified radix.

- ``valueOf()``.

- ``toLocaleString()``

Boolean
-------

- boolean primitive type's object counterpart.

- constructor function: ``Boolean()``.

- 注意在 boolean 环境下, 根据 `ToBoolean`_, Boolean instance 由于是 object,
  所以是 truthy 的.  这与 boolean primitive 不同::

    !(new Boolean(false)) // false

Array
-----
- literal form::

    [a, b, ...]
    [a, , b, ...]

  sparse array (i.e. array with unfilled slots) can be created with second
  form. 注意末尾的 ``,`` 不会识别为后侧还有 slot. 每个 ``,`` 只影响左侧::

    [1,,,2,] // [1,,,2,]

- In JS, Arrays are list-like high-level objects.

- array index.

  * A valid array index is a non-negative integer.

  * Formally, array indices are just array object's normal properties.
    Therefore indices are actually strings. A integer index is firstly
    coerced to string (via `ToString`_) before used to access array element.::

      var x = ['a', 'b', 'c'];
      x[1]; // 'b'
      x['2']; // 'c'

    但是只有 numerical index 或 numerical formed string index 会影响 array
    length.

- Because array is object, it is theoretically possible to use array like
  an object, i.e., save named property in an array object.::

    > var x = [];
    undefined
    > x.sef = "xxx";
    'xxx'
    > x
    [ sef: 'xxx' ]
    > x[0]='rrr';
    'rrr'
    > x
    [ 'rrr', sef: 'xxx' ]
    > x[2]='yyy';
    'yyy'
    > x
    [ 'rrr', <1 empty item>, 'yyy', sef: 'xxx' ]
    > x['bbb'] = 'aaa';
    'aaa'
    > x
    [ 'rrr', <1 empty item>, 'yyy', sef: 'xxx', bbb: 'aaa' ]

  However, this would generally be considered improper usage of the respective
  types. Because arrays have behavior and optimizations specific to their
  intended use.

- Sparse array. 由于 index 本质只是 array object 的 property name, 所以:

  * 当给 array 非连续 index 赋值时, 中间没有赋值的 index 并不存在.

  * When you delete an array element, the array length is not affected.
    因为本质上是删除了一个名为 index 数值的 property. 被删掉的 index 不再
    存在, 但其他内容并不自动更新.

  * 如果 Array 的 sparse array 属性 is undesirable, and dense array is
    required, use typed arrays.

constructor
^^^^^^^^^^^
::

  new Array(elem0, elem1, ...)
  new Array(length)
  Array(...)

- If the only argument passed to the Array constructor is an integer between
  0 and 2**(32-1) (inclusive), this returns a new JavaScript array with its
  length property set to that number. (WTFJS_) Which is a stupid terrible idea.

- 如果要避免歧义, 使用 ``Array.of()`` static method.

- 有没有 new operator, 效果都一样.

static attributes
^^^^^^^^^^^^^^^^^
- @@species, Symbol.species.

static methods
^^^^^^^^^^^^^^

- ``from(array_like_or_iterable[, mapfunc[, <this>]])``. Create an array by
  shallow-copying elements from an array-like object or iterable object.

  * ``mapfunc``. elements are optionally processed through ``mapfunc``.
    signature::

      function mapfunc(value, index) {
          //
      }

  * ``this``. The function will be bound to ``this`` if it is spcified.

  * ``Array.from`` is a class method, it use current class's constructor to
    create the new array. 因此, 子类调用该方法自动生成子类实例.

- ``isArray(obj)``. test whether obj is Array instance. Mostly irrelevant
  except across iframes (?). instanceof do just fine in most cases.

- ``of(elem0, elem1, ...)``. 无歧义版的 Array constructor.

attributes
^^^^^^^^^^
- ``length``. The length of array which is an unsigned 32-bit integer that is
  greater than the highest index in the array.

  If array's highest numerical index is changed, its length is adjusted
  automatically. It does not care the sparsity of the array.

  ``length`` property is writable. 修改 length 值直接影响 array 的实际长度.
  若变短, 多余的元素直接舍去.

- N. numerical index.

methods
^^^^^^^

iteration
""""""""""
- @@iterator, Symobol.iterator. Returns an ``Array Iterator`` yielding array
  values. This makes Array objects iterable.

- ``values()``. ditto.

- ``forEach(<callback>[, <this>])``. Run callback for each element. Returns
  undefined. callback's signature: current element, current index, the array
  itself. callback's ``this`` can be bound to ``<this>``, which defaults to
  undefined.

  * There is no way to stop or break a forEach() loop other than by throwing an
    exception.

  * behavior of array modification during iteration.

    - The *range* of elements processed by forEach() is set before the first
      invocation of callback.

    - 遍历到某个 index 时, 取的是该 index 上的最新元素值, 所有之前的修改都可见.

    - elements that are deleted before being visited are not visited.

  * holes in sparse array is skipped.

- ``entries()``. returns an ``Array Iterator`` that yields ``[index, value]``
  pairs. This is like ``enumerate()`` in python.

  * holes in sparse array is not skipped.

- ``filter(testfunc[, <this>])``. Filter out an array of values that passes the
  test. Signature of ``testfunc``: ``(element, index, array)``.

  * holes in sparse array is skipped.

- ``keys()``. return an ``Array Iterator`` that yields array's filled *and*
  unfilled indices. This differs from ``Object.keys()`` in that the form includes
  all integers from ``[0, ..., length-1]``, while the latter cares only about
  numerically named properties that are actually present.

  * holes in sparse array is not skipped.

- ``map(mapfunc[, <this>])``. returns a new array with the results of applying
  mapfunc on every elements of the array.

  * holes in sparse array is not skipped.

- ``reduce(callback[, initial])``.

  * holes in sparse array is skipped.

- ``reduceRight(callabck[, initial])``

  * holes in sparse array is skipped.

element
""""""""
- ``indexOf(elem[, start])``

  * holes in sparse array is skipped.

- ``lastIndexOf(elem[, start])``

  * holes in sparse array is skipped.

- ``find(testfunc[, <this>])``.

  * holes in sparse array is not skipped.

- ``findIndex(testfunc[, <this>])``. ditto for index.

  * holes in sparse array is not skipped.

testing
""""""""
- ``some(<callback>[, <this>])``. tests whether at least one element in the
  array passes the test. 参数意义 ditto. Returns true if the callback function
  returns a truthy value for any array element; otherwise, false.

  * callback signature: ``callback(value, index, array)``

  * Once a truthy return value is realized, ``some()`` immediately returns true.

  * holes in sparse array is skipped.

- ``every(...)``. whether all elements pass the test. All else ditto.

  * holes in sparse array is skipped.

- ``includes(elem[, start])``. test elem in array.

  * holes in sparse array is not skipped.

generating new stuff
""""""""""""""""""""
- ``slice([begin[, end]])``. Return a slice of array into a new array. Like
  iterable slicing syntax in python ``[begin:end]``.

  * negative indices can be used to count from the end of array.

  * If begin is undefined, default to 0.

  * If end is undefined, default to length.

  * If begin is greater than or equal to end, empty array is returned.
    If begin is greater than or equal to length, empty array is returned.

  * ``slice()`` 可以作用在 array-like object 上, 用于将它们转换成真正的
    Array object. By binding ``Array.prototype.slice()`` function to the
    object::

      let args = Array.prototype.slice.call(arguments);
      let args = [].slice.call(arguments);

  * holes in sparse array is not skipped.

- ``concat(elem_or_array, ...)``

  * holes in sparse array is not skipped.

- ``join([sep])``

  * holes in sparse array is not skipped.

array-wide manipulation
"""""""""""""""""""""""
- ``copyWithin(target[, start[, end]])``

  * holes in sparse array is not skipped.

- ``fill(value[, start[, end]])``. fill with static value.

  * holes in sparse array is not skipped.

- ``splice(start[, deleteCount[, item1, ...]])``. 删除一部分, 插入一部分.

  * holes in sparse array is not skipped.

ordering
""""""""
- ``reverse()``

  * holes in sparse array is not skipped.

- ``sort([comp])``. default comparison function compares elements' `ToString`_
  value.

  * holes in sparse array is not skipped.

head or tail manipulation
""""""""""""""""""""""""""
- ``pop()``

  * holes in sparse array is not skipped.

- ``push()``

  * holes in sparse array is not skipped.

- ``shift()``

  * holes in sparse array is not skipped.

- ``unshift()``

  * holes in sparse array is not skipped.

conversion
""""""""""

- ``toString()``. string representation which is ``elem1,elem2,...``

  * holes in sparse array is not skipped.

- ``toLocaleString()``

  * holes in sparse array is not skipped.

Function
--------

- A function is a callable object. It has the internal ``[[Call]]`` method
  so that the object can be called.

- literal form: function declaration, function expression and arrow function
  expression.

- constructor ``Function()``.

- A function is a callable object. In JS, function is first-class entity like
  normal objects.

- function object can store properties like normal object. This is sometimes
  useful::

    > function x() {}
    undefined
    > x
    [Function: x]
    > x.r
    undefined
    > x.r=1
    1
    > x
    { [Function: x] r: 1 }
    > x.p=2
    2
    > x
    { [Function: x] r: 1, p: 2 }

constructor
^^^^^^^^^^^
::

  new Function([arg1[, arg2, ...]], body)
  Function([arg1[, arg2, ...]], body)

- Constructor works the same with or without ``new`` operator.

- ``argN`` 是参数名称, in string. ``body`` is function body in stirng.

  ``body`` is ``eval()``-ed. function body will only be able to access their
  own local variables and global ones, not the ones from the scope in which the
  Function constructor was called.

attributes
^^^^^^^^^^
- ``length``. readonly data property. the number of positional args expected by
  function.

  * This number excludes the rest parameter and only includes parameters before
    the first one with a default value.

- ``name``. function's name or ``anonymous`` if function is created
  anonymously.

methods
^^^^^^^
- ``call([<this>, arg1[, ...]])``.
  call the function with specified ``this`` and args.

  * In non-strict mode, if ``this`` is ``null`` or ``undefined``, it will
    be replaced with the global object.

  * primitive values will be autoboxed.

- ``apply([<this>, [args-array]])``.
  call function with specified ``this`` and array-like list of args.
  Otherwise it's the same as ``call()``.

  * ``apply()`` is useful when args are passed as an array-like object
    rather than individual elements (或者使用 ``...`` operator.)

- ``bind(<this> [, arg1[, ...]])``.
  Create a bound function of original function, also optionally partially
  applying arguments.

  * In non-strict mode, if ``this`` is ``null`` or ``undefined``, it will
    be replaced with the global object.

    如果确实不需要 bind effect, 只需要 partial application, 可传一个 empty
    object 作为 ``this``, 避免 side effect on global object.::

      var ø = Object.create(null);

  * The returned bound function cannot be re-bound.

  * The bound ``this`` value is ignored if the bound function is used as
    constructor following the ``new`` operator. While the partially applied
    args are still used.

  * the result bound function's ``name`` attribute is ``bound <func>``.

  * the result function can not only be bound, but also partially applied.

  * The bound function does not have ``prototype`` property. In cases where
    prototype is required, the original function's ``prototype`` is used,
    e.g. during ``new`` instantiation; ``instanceof`` testing.

RegExp
------

- literal form: ``/pattern/[flags]``

- constructor function: ``RegExp()``

- The literal form is prefered to constructor form because the JS engine
  precompiles and caches them before code execution. 例如在 loop 中创建的
  regexp literal 只编译一次, 且在 compile time.

  Constructor form is useful to dynamically build regexp object.

- flags.

  * g. global match. find all matches

  * i. ignore case.

  * m. multiline. ``^$`` chars also match the begin and end of each line.

  * u. treat pattern as a sequence of unicode points. 对 js 来说, 这看上去很
    必要啊.

  * y. sticky. The sticky flag advances lastIndex like g but only if a match is
    found starting at lastIndex, there is no forward search. The sticky flag
    was added to improve the performance of writing lexical analyzers using
    JavaScript.[SOJSRESticky]_

- 注意 ``g`` flag 的使用需要配合对一个 RegExp object 的多次复用, 才能体现出价值.
  例如在 for loop 中使用.::

    let re = /pattern/g;
    let match;
    while (match = re.exec("string") !== null) {
        if (!match) {
            break;
        }
        // processing next match.
    }

constructor
^^^^^^^^^^^
::

  new RegExp(pattern[, flags])
  RegExp(pattern[, flags])

- pattern can be regexp pattern string, or a RegExp object.

- flags will be added to pattern. If pattern carries own flags, they'll be
  replaced by the specified flags.

- 为了避免 escape regexp escape sequence, 可使用::

    new RegExp(String.raw`pattern`)

- constructor can be used with or without new operator.

attributes
^^^^^^^^^^
- source. pattern text.

- flags. flags string.

- global. whether the RegExp object is global.

- ignoreCase. ...

- multiline. ...

- unicode. ...

- sticky. ...

- lastIndex. (WTFJS_) An writable property that *unbelievably* keeps the last
  index at which to start the next match. 这太牛逼了, 在 RegExp instance 上
  记录匹配结果状态. 给力!! (WTFJS_, WTFJS_, WTFJS_)

  lastIndex is modified only if "g" or "y" flag is set. 这是用于在一个字符串上
  进行多次匹配, 每次返回不同部分的匹配结果. 由于 js regexp 不像 python 提供
  ``re.findall()`` API, 所以只能用这种方式.

  WATCH OUT FOR THIS PITFALL::

    > re = /sef/g
    /sef/g
    > re.exec('sef')
    [ 'sef', index: 0, input: 'sef', groups: undefined ]
    > re.exec('sef')
    null
    > re.exec('sef')
    [ 'sef', index: 0, input: 'sef', groups: undefined ]
    > re.exec('sef')
    null

methods
^^^^^^^

- ``exec(str)`` search str for pattern, return result array or null if unmatch.

  result array.

  * index 0: the matched substring.

  * index 1-N: one item for each matched capturing groups.

  * index. start index of the match.

  * input. the input string.

- ``test(str)``. As with exec(), test() called multiple times on the same
  global regular expression instance will advance past the previous match.

- ``Symbol.match``. used internally by ``String.prototype.match``. also used to
  determine if an object may be used as a regular expression.

- ``Symbol.search``. ditto for search.

- ``Symbol.replace``. ditto for replace.

- ``Symbol.split``. ditto for split.

- ``toString()``. return ``/pattern/flags`` form.

Date
----

- constructor function: ``Date()``

constructor
^^^^^^^^^^^
::

  new Date()
  new Date(milliseconds)
  new Date(dateobj)
  new Date(datestring)
  new Date(year, month[, day[, hours[, minutes[, seconds[, milliseconds]]]]])
  Date(...)

- Without new operator, returns a string representing the current date and time,
  in the same format as ``Date.prototype.toString()``.

- The argumentless form returns current date and time in local timezone.

- The milliseconds form use Unix epoch as starting point.

- The dateobj form returns a new Date object with the same date and time.

- The datestring form is equivalent to ``Date.parse()`` class method.

- The year, month, ... format form

  * ``year``. Values from 0 to 99 map to the years 1900 to 1999.

  * ``month`` is 0-based.

  * if values are greater than their logical range, they are normalized within
    the logical range, with the adjacent value adjusted.

  * date and time args are interpreted in local timezone.

  * missing params are set to appropriate starting calendar value.

static methods
^^^^^^^^^^^^^^

- ``now()``. returns current date time in milliseconds since epoch.

- ``parse(datestring)``. parse string into milliseconds since epoch or NaN if
  string can not be parsed.

  formats: rfc2822, iso8601.

- ``UTC(year, month[, day[, hours[, minutes[, seconds[, milliseconds]]]]])``.
  arguments are parsed in UTC timezone. return milliseconds since epoch.

methods
^^^^^^^
The naming of APIs is just perfect (WTFJS_).

- ``getFullYear()``, ``getUTCFullYear()``, ``setFullYear(year[, month[, day]])``, ``setUTCFullYear()``

- ``getMonth()``, ``getUTCMonth()``, ``setMonth(month[, day])``, ``setUTCMonth()``

- ``getDate()``, ``getUTCDate()``, ``setDate(day)``, ``setUTCDate()``. day of month

- ``getHours()``, ``getUTCHours()``, ``setHours(hours[, minutes[, seconds[, ms]]])``, ``setUTCHours()``.

- ``getMinutes()``, ``getUTCMinutes()``, ``setMinutes(minutes[, seconds[, ms]])``, ``setUTCMinutes()``.

- ``getSeconds()``, ``getUTCSeconds()``, ``setSeconds(seconds[, ms])``, ``setUTCSeconds()``.

- ``getMilliseconds()``, ``getUTCMilliseconds()``, ``setMilliseconds(ms)``, ``setUTCMilliseconds()``.

- ``getDay()``, ``getUTCDay()``. day of week

- ``getTime()``, ``setTime(time)``

- ``getTimezoneOffset()``

- ``toString()``. format::

    %a %b %d %Y %H:%M:%S %Z%z (timezone name)

- ``toDateString()``. returns the date part in string.

- ``toTimeString()``.

- ``toISOString()``.

- ``toUTCString()``

- ``toLocaleString()``

- ``toLocaleDateString()``

- ``toLocaleTimeString()``

- ``toJSON()``

- ``valueOf()``. return milliseconds since epoch.

Error
-----

- Base error class.

- constructor function: ``Error()``

constructor
^^^^^^^^^^^
::

  new Error([msg])
  Error([msg])

- An Error instance is created with or without new operator.

attributes
^^^^^^^^^^

- name. name of error class.

- message.

- stack. stack trace of exception. will be generated as soon as the error is
  instantiated.

methods
^^^^^^^

- ``toString()``. format::

    `${error.name}: ${error.message}`

abstract operations
===================

type coercion
-------------
- implicit type coercion is designed to help you!!! (WTFJS_) But it can create
  confusion if you haven't taken the time to learn the rules that govern its
  behavior.

- type coercion is implemented by calling various abstract operations.
  实际上可以理解为调用各个类型的 constructor function 进行类型转换.

ToBoolean
^^^^^^^^^
- Undefined: false.

- Null: false.

- Boolean: argument.

- Number:

  * +0, -0, NaN: false.

  * otherwise: true.

- String:

  * emptry string: false.

  * otherwise: true.

- Symbol: true.

- Object: true.

ToNumber
^^^^^^^^

- Undefined: NaN

- Null: 0

- Boolean: true 1, false 0.

- Number: argument.

- String:

  * numeric literal in string form, possibly surrounded by whitespace chars
    are converted to corresponding number.

    numeric literal can be in decimal, octal, hex, or binary format.

  * empty string or string with only whitespace chars are converted to 0.

  * strings can not be parsed converted to NaN.

- Symbol: TypeError

- Object: `ToPrimitive`_ then `ToNumber`_.

iteration, generation and asynchronous programming
==================================================

- js 中的 iterable, iterator, generator function, generator 与 python
  中的概念是基本一致的, 只是实现方式有些差异而已.

iterable protocol
-----------------
- iterable: an object (or one of the objects up its prototype chain) that
  implements the @@iterator method, which returns an iterator object.

- The @@iterator method can be implemented by:

  * a normal function that manually returns a iterator object.

  * a generator function that, when called, returns a generator object
    (which is also an iterator) automatically.

- Whenever an object needs to be iterated, its @@iterator method is called with
  no arguments, and the returned iterator is used to obtain a sequence of values
  to be iterated.

- the @@iterator key is refered as ``Symbol.iterator``.

- builtin iterables:

  * String. iterates through string's characters.

  * Array. iterates through array's elements.

  * TypedArray.

  * Map.

  * Set.

- iterable protocol is useful in various circumstances. e.g.:

  * for-of statement.

  * spread syntax ``...``::

      [..."sef"] == ["s", "e", "f"]

  * delegated yield statement: ``yield*``.

  * destructuring assignment.

  * various container object constructors. e.g., Map(), Set(), etc.

iterator protocol
-----------------
- iterator protocol defines a standard way to produce a sequence of values.

- iterator: an object that implements a ``next()`` method that returns an
  object on each call. The returned object has the following attributes:

  * value. the produced value. can be omitted when ``done`` is true.

  * done. a boolean that is true if the iterator is past the end of the
    iterated sequence; false if the iterator is able to produce more value,
    in which case done property can be omitted.

  If non-object is returned by iterator's ``next()`` method, TypeError is
  raised.

generator function
------------------

- A GeneratorFunction is a special type of function that works as a factory for
  generator iterators.

- Use ``function*`` keyword to define a generator function.

- generator function 中支持 ``yield*`` expression to delegate generation to
  another iterable, 注意是 iterable 即可, 无需是 iterator (会自动生成). The
  value of ``yield*`` expression itself is the value returned by the created
  iterator when it's closed.

generator
---------

- A generator object is both an iterable and an iterator.
  Its @@iterator method simply returns itself.::

    function* f() {yield 1;}
    let g = f();
    g[Symbol.iterator]() === g

- A generator function's return value or ``generator.return(value)`` method
  传入的值是一个 generator 对应于 ``done: true`` 时的值. 注意这个值本身不属于
  generator 生成的 value list 的一部分. (这类似于 python 中 generator function
  的 return value 只是 StopIteration 的参数.) 例如:

  .. code:: javascript

    function* f() {
        yield 1;
        yield 2;
        return 3;
    }

    for (const v of f()) {
        console.log(v);
    }
    // 1, 2

- Exception thrown inside the generator make the generator finished, unless it
  is caught within the generator's body.

methods
^^^^^^^
- ``next([value])``. ``value`` 值是 send to generator 内部的一个值, 用于影响
  generator 的行为. 这个值成为 yield expression 的值. 不设置时, 默认值为
  undefined. Return an object conforming to iterator protocol's requirement.

  与 python generator 相比, ``next()`` method 结合了 python 中 generator 的
  ``__next__`` & ``send(value)`` method. 感觉更方便一些.

  对一个 generator, 第一次执行 ``next()`` 时, 启动 generator 运行. 此时传入
  value 并无意义.

- ``return([value])``. returns ``{"value": value, "done": true}`` and closes
  the generator. ``value`` defaults to undefined. If the generator is already
  closed, its state is not changed.

  这对应于 python 中 ``generator.close()``, 但更灵活一些.

- ``throw(exception)``. throw ``exception`` from the point where the execution
  was paused in the generator. Return the next item (or exit at its will). If
  the generator function does not catch the passed-in exception, or raises a
  different exception, then that exception propagates to the caller.

async, await
------------
- Async functions generators and promises in a higher level syntax. Please
  understand that they work essentially under the same principle.

Array-like object
-----------------
An array-like object is one that has a ``length`` property of a non-negative
integer, and some indexed properties. [SOArrayLike]_

When an array-like object is used under context where array is required, the
list of values is generated by accessing index properties from 0 to length.
Much like the following::

  values = [];
  for (let i = 0; i < obj.length; i++) {
      values.append(obj[i]);
  }

So, in a sense, ``{length: 5}`` is an array-like object.


statements
==========
In js, statement normally ends with ``;``.

declarations and variable statements
------------------------------------
- Declarations create variables. Variables must be declared before being used.

- In JS, compiler only declares variables in scope during compilation stage;
  it's engine's job to assign variable to the specified value during runtime.

  Thus for a variable declaration with initial value, it's equivalent to two separate
  statement and executed separately (in different execution stage)::

    var x = 1;
    // ---
    var x; x = 1;

  Note: variables are declared at compile-time, doesn't mean variables can be
  referenced before reaching declaration statement at runtime. This hoisting
  behavior is only specific to ``var`` declaration.

  In other words, for ``var`` declarations, the following two are equivalent::

    function foo() {
        console.log(x);
        var x = 1;
    }

    function foo() {
        var x;
        console.log(x);
        x = 1;
    }

  But for ``let``, ``const`` declarations, hoisting does not happen at all::

    function foo() {
        console.log(x);
        let x = 1;
    }

    function foo() {
        console.log(x);
        let x; x = 1;
    }

  It is only for ``var`` statement that the declared variable is made available
  to entire scope; for ``let``, ``const`` statements, the declared variable is
  only available from the point of declaration until the end of scope.

let
^^^
::

  let var1 [= value1] [, var2 [= value2]] ...;

- ``let`` declaration create variables that respect block scope.

- Within the same scope, duplicated ``let`` declarations raise ``SyntaxError``.

- Temporal dead zone (TDZ). ``let``-declared variables are only visible from
  the point of declaration until the end of block scope. from the beginning of
  block scope until before the point of declaration is called the variable's
  TDZ.

  Effects of TDZ:

  * Because of TDZ, ``let`` does not do hoisting.
    ``let`` declaration don't do hoisting::

      function foo() {
          console.log(x); // raise ReferenceError.
          let x = 1;
          console.log(x);
      }

  * Because of TDZ, using the ``typeof`` operator to check for the type of a
    variable in that variable's TDZ will throw a ``ReferenceError``, unlike
    those simply undefined variables.

  * Note TDZ starts from beginning of scope until the point of ``let`` **lvalue**
    resolution. some confusing examples::

      function test(){
         var foo = 33;
         if (true) {
            let foo = (foo + 55); // ReferenceError, rvalue `foo` still in TDZ.
         }
      }
      test();

      function go(n) {
        // n here is defined!
        console.log(n); // Object {a: [1,2,3]}

        for (let n of n.a) { // ReferenceError. this `n` is declared in an implicit block
          console.log(n);    // via ``let n = n.a;`` which makes rvalue `n.a` in TDZ.
        }
      }

      go({a: [1, 2, 3]});

- advantages to declaring variables using block scope.

  * the principle of least privilege/exposure.

  * to be more memory-efficient. out of scope stuffs are garbage-collected.

const
^^^^^
- const is just like let, except that the const-declared variables are read-only.
  Any attempt to modify its value will raise a ``TypeError`` exception.

var
^^^
::

  var var1 [= value1] [, var2 [= value2]] ...;

- **let is new var. Stop using var.** (ES6)
  There is basically no use for ``var`` given ``let`` is available.

- variables declared by ``var`` have function scope or global scope, but not
  block scope.

- Within the same scope, duplicated ``var`` declarations are ignored (WTFJS_).
  But note the assignment is not ignored.

- hoisting. Wherever a ``var`` appears inside a scope, that declaration is
  taken to belong to the entire scope and accessible everywhere throughout
  (WTFJS_).

  It is effectively equivalent to say ``var`` declarations are displaced to
  the top of the current effective scope. If variable is initialized at
  declaration, the initialization part remains at the original location::

    function foo() {
        console.log(x); // undefined
        var x = 1;
        console.log(x); // 1
    }

    // equivalent to

    function foo() {
        var x;
        console.log(x);
        x = 1;
        console.log(x);
    }

  Note that only declaration is hoisted, assignment part is left in place.
  Otherwise, program logic would be different.

  Var hoisting should NOT be relied upon.

destructuring assignment
------------------------
::

  let [a, b] = [1, 2];
  let [a, b, ...c] = [1, 2, 3, 4];

  let {x, y} = {x:1, y:2};
  ({a, b, ...c} = {x:1, y:2, z:3, w:4});
  let {x: p, y: q} = {x:1, y:2};

- 如果 LHS 变量数多于 RHS unpacking 的值的数目, 即 LHS 不能全部赋值,
  剩下的会使用默认值.::

    let [a,b, ...[c, d, ...e]] = [1,2,[3,4,5,6]]
    // c: [3,4,5,6]
    // d: undefined
    // e: []

  如果 LHS 少于 RHS, 多余的 RHS 值直接抛弃.

  这些方面与 python 中不同.

- LHS 的各变量支持设置默认值, 当没有 RHS 中相应的项赋值, 则使用默认值, 默认的
  默认值是 undefined.::

    [a=1, b=2, c=3] = [4, 4]; //a:4, b:4, c:3
    ({a, b, c:d=3} = {a:1, b:2});

  rest parameter 不支持设置默认值.

- unneeded unpacking values can be ignored by leaving the corresponding LHS
  position empty. 这与 python 中不同.::

    [a,,b] = [1,2,3,4,5]

  object destructuring 不支持这种形式.

- nested destructuring assignment.

  * for array destructuring.::

      [a, [b, [c, d]]] = [1, [2, [3, 4]]];

  * for object destructuring.::

      ({a:aa, b: {c: cc, d: dd}} = {a:1, b: {c: 3, d: 4}});

- destructuring assignment, 尤其是比较复杂的, 例如涉及 nested, 涉及 array &
  object destructuring, 涉及使用 ignored parameter, rest parameter, etc,
  很适合用于从数据结构中提取所需信息. ::

    var metadata = {
        title: 'Scratchpad',
        translations: [
           {
            locale: 'de',
            localization_tags: [],
            last_edit: '2014-04-14T08:43:37',
            url: '/de/docs/Tools/Scratchpad',
            title: 'JavaScript-Umgebung'
           }
        ],
        url: '/en-US/docs/Tools/Scratchpad'
    };

    var {title: englishTitle, translations: [{title: localeTitle}]} = metadata;

    console.log(englishTitle); // "Scratchpad"
    console.log(localeTitle);  // "JavaScript-Umgebung"

object destructuring
^^^^^^^^^^^^^^^^^^^^
- object destructuring 的一般形式::

    let {<var>[:<newvar>][=<default>], ...} = <object>
    ({<var>[:<newvar>][=<default>], ...} = <object>)

- 当 newvar 未指定时, 默认为 var; 当 default 未指定时, 默认为 undefined.

  如果 object 中要赋值的 key 不是 valid identifier, 即只能以 string 形式
  写出, 则必须设置 valid identifier newvar 来接受对应值. 例如::

    let {'var-': var} = {'var-': 1};

- 赋值的是 newvar. 若使用声明并初始化形式, 声明并初始化的是 newvar.

- object destructuring 是将属性值赋值给 LHS 对应位置的映射参数的值, 因此在
  LHS 不关心变量的书写顺序. 只有在 RHS unpacking 时具有的属性才会被赋值,
  否则使用默认值. 如果包含 rest parameter, 剩下的成为 rest object 的属性.

- 对于 object 的 destructuring assignment, 若不是在声明时初始化, 则必须添加 ``()``,
  这是 js 词法分析限制导致的: ``{}`` on the left-hand side is considered a
  block and not an object literal.

- 在省略 ``;`` 的情况下, ``()`` wrapper 可能导致误当作函数参数. 但省略
  semicolon 本来就是不对的.

- object destructuring 允许用在函数参数部分, 用来模拟 keyword-only parameters
  with default value. 这是相当奇怪的语法.::

    let f = ({a=1, b=2}={}) => {
        //
    }

block statement
---------------
::

  { [statements] }

- AKA compound statement.

- a block statement can be used anywhere a normal statement can. e.g.::

    var a = 1, b = 2; {
        console.log(a);
    }

- lexical scoping rules:

  * Variables declared with ``var`` do not have block scope.

  * Variables declared with ``let`` and ``const`` do have block scope.

- ``}`` marks the end of a block statement. Any other statement is free to show up
  after that. E.g.::

    {
        console.log(1);
    } let a=1; {
        console.log(a);
    } {
        console.log(a);
    }

conditional statements
----------------------

if statement
^^^^^^^^^^^^

switch statement
^^^^^^^^^^^^^^^^

iteration statements
--------------------

while statement
^^^^^^^^^^^^^^^

do-while statement
^^^^^^^^^^^^^^^^^^

for statement
^^^^^^^^^^^^^
- for loop 实际上创建了两个 block scope. header 位于 outer block,
  loop body 是 inner block.::

    for (<h1>; <h2>; <h3>) {
        <body>
    }
    // conceptually similar to
    {
        <h1>
        while (<h3>) {
            <body>
            <h2>
        }
    }

  In other words, 在 header 中创建的变量, 只创建一次. 在各次循环中
  可用.

- ``let`` for loop vs ``var`` for loop.

  * let confines loop variables in block scope, which is good.

  * let for loop has a weird rebinding behavior, which should be avoided.
    在每次循环进入 body block 时, 与 header variable 同名的变量被创建,
    初始化为 loop variable 当前值. 在退出 body block 时, 该变量的当前值赋值
    给 loop variable. [SOLetLoop]_ (WTFJS_)::

      for (let i = 0; i < 3; i++) {
          console.log(i);
      }
      // prints 012
      // equivalents to the following sanity version
      for (let i = 0; i < 3; i++) {
          let j = i;
          console.log(j);
          i = j;
      }

for-in statement
^^^^^^^^^^^^^^^^
::

  for ([var|let|const] <var> in <obj>) {

  }

- for...in iterates over the enumerable property's name of an object itself and
  those the object inherits from its constructor's prototype.  The properties
  of an object is iterated in an arbitrary order.

  注意 Symbol properties 不会包含.

- 对于 array, 注意由于 for...in 在 iterate array 时是把它当作 object
  去遍历, 因此 indices 不保证按顺序出现. 并且如果有其他不属于 index 的
  enumerable property 则也会出现在 iteration 中.

  因此对于 array, 应使用 normal for statement 配合 array.length, 或者使用
  for...of statement.

- For ``(var|let|const) <var>`` form, ``<var>`` is re-declared for each
  iteration of loop. This is equivalent to::

    let keys = Object.keys(<obj>);
    for (let i = 0; i < keys.length; i++) {
        (var|let|const) <var> = keys[i];
        ...
    }

- ``const`` is useful to prevent loop variable getting modified in loop body.

- 注意在 for-in loop 的 ``<var>`` 赋值语句, 支持所有一般形式的声明初始化
  statement, 包含普通的变量初始化语句与 destructuring assignment statement.

for-of statement
^^^^^^^^^^^^^^^^
::

  for ([var|let|const] <var> of <obj>) {

  }

- for...of statement creates a loop iterating over iterable objects.
  It iterates over data that iterable object defines to be iterated over.

- for...of statement is very useful for iterating elements of Array etc.

- For ``(var|let|const) <var>`` form, ``<var>`` is re-declared for each
  iteration of loop.

- 注意在 for-of loop 的 ``<var>`` 赋值语句, 支持所有一般形式的声明初始化
  statement, 包含普通的变量初始化语句与 destructuring assignment statement.

flow control statements
-----------------------

return statement
^^^^^^^^^^^^^^^^

try statement
-------------
::

  try {
    ...
  }
  catch (exc) {
    ...
  }
  finally {
    ...
  }

- at least one of ``catch`` and ``finally`` must be present with ``try``.

- ``catch`` block creates a block scope. The ``exc`` exception variable
  is declared in the block scope, thus not available outside of it.

- JS does not support multi-catch statement based on exception class, as
  they do in Python. We can manually construct it using conditionals::

    try {
        ...
    }
    catch (e) {
        if (e instanceof ...) {
            ...
        }
        ...
        else {
            ...
        }
    }

function statements
-------------------

Including function declaration statements, generator function declaration
statements, See `function`_.

with statement
--------------
**deprecated.**

It makes compiler disable compile-time optimization, leading to slower code.

In strict mode, ``with`` statement is disallowed.

expressions
===========

- operators::

    + - * / %
    = += *= /=
    ++ --
    . []
    == === != !==
    < > <= >=
    && ||

additive operators
------------------

addition (+) operator
^^^^^^^^^^^^^^^^^^^^^
- 两种操作: string concatenation or numerical addition.

  * 当两个 operand 中至少有一个的值是 string 类型时, 进行 strint concatenation.
    此时, 将另一个 operand 也转换成 string, 然后 concatenation. 生成一个 string
    primitive typed value.

  * 所有其他情况都进行 numerical addition.

- 对于 object type operands, 首先转换成 primitive. 然后才判断进行哪种操作.

bitwise operators
-----------------
- Only defined for the lower 32 bits of numbers. Meaning the higher 32 bits of
  the operands are just ignored. (WTFJS_)

multiplicative operators
------------------------

division (/) operator
^^^^^^^^^^^^^^^^^^^^^

- divide-by-zero. In JS, this is not an exceptional condition. Instead, positive
  or negative infinity is returned::

    1/0 // Infinity
    -1/0 // -Infinity

- infinity divides by infinity. NaN.

Primary expression
------------------

this keyword
^^^^^^^^^^^^
- ``this`` can not be assigned directly. It is a special keyword, rather than
  a variable (unlike ``self`` in python). Its value is assigned by JS engine,
  and dependent on its current runtime environment.

- the value of ``this``.

  * global context. ``this`` refers to global object.

  * function context. depends on how function is called (call-site and context
    object). 无论使用下述哪种方式, 如果最终传入 function body 的 ``this`` value
    是 undefined, 在 non-strict mode 会转换成 global object (WTFJS_); 在 strict
    mode 保持 undefined.

    - simple call. ``this`` defaults to undefined, except when its value is
      set by the call. 在 non-stirct mode, 变成 global object.

    - called via a context object's method reference. ``this`` is set to the
      context object.

      注意如果 method reference 之后没有直接 call function, 而是通过 simple
      call 的方式去调用, 这是符合 simple call 的情况的. 此时 ``this`` 是 undefined.
      这是因为无论函数在哪里定义 (单独声明, 还是在 object attribute 赋值
      function expression), 创建的结果都是相同的 function object.
      只有调用的方式最终决定 ``this`` binding.::

        var x = {};
        var m = function () { console.log(this) };
        x.m = m;
        x.m(); // {m: [Function]}
        var y = x.m;
        y(); // global object or undefined.

    - with explicit binding,
      ``Function.prototype.call()``, ``Function.prototype.apply()``. set
      ``this`` value for function call. 这个用法相当于在 python 中, 给 class
      unbound method 传递 self 对象来直接调用. 假装对象有这个方法.

      Explicit binding takes precedence over context object's method reference.::

        obj.foo.call(obj2) // this -> obj2

    - with hard binding,
      ``Function.prototype.bind()``. create a new function with ``this`` bound
      to the specified object, regardless how the new function is being used.

    - with ``new`` binding, i.e., as a constructor. ``this`` is bound to the
      new object being created.

      New binding takes precedence over context object's method reference and hard
      binding.::

        let obj2 = new obj.foo() // this -> obj2
        let obj3 = new (obj.foo.bind(obj))() // this -> obj3

    - as a DOM event handler. ``this`` is set to the element the event fired from.

    - When ``this`` appears in an inline event handler, ``this`` is set to the DOM
      element on which the listener is placed. Note only the outer code has its
      ``this`` set this way.

  * arrow function. In arrow functions, ``this`` retains the value of the enclosing
    lexical scope's ``this``.

left-hand-side expressions
--------------------------

function call expression
^^^^^^^^^^^^^^^^^^^^^^^^
::

  <call-expression> ( [argument-list] )

``(...)`` indicates ``<call-expression>`` should be executed, thus requires it callable.
Otherwise, ``TypeError`` is raised.

new operator
^^^^^^^^^^^^
::

  new Func(<args>)

- new operator instantiates a instance of constructor.

- In JS, constructors are normal functions that called after ``new`` operator.
  We can say ``new func()`` is the ``func``'s constructor call.

- Func 在实例化过程中的作用.

  * Func.prototype is linked as the prototype of the created object.

  * called to initialize the object created by ``new`` operator.

- During constructor call, the following happens,

  * a new object is created

  * the newly constructed object is prototype-linked

  * constructor function is called to initialize the object, by its setting ``this`` to
    the object.

  * the newly constructed object is returned as value of the ``new`` expression, unless
    the constructor returns alternative object itself.

- a bound method's instance is also the original function's instance. the bound ``this``
  is ignored, but other partial applied arguments are preserved.::

    var f2 = func.bind(obj);
    var ins = new f2();
    ins instanceof f2; // true
    ins instanceof func; // true

unary operators
---------------

typeof
^^^^^^
- return string name of the type of the operand.

- output of different types of objects.

  - Undefined: "undefined"

  - Null: "object". **Note** it's not "null"[1]_ (WTFJS_).

  - Boolean: "boolean".

  - Number: "number"

  - String: "string"

  - Symbol: "symbol"

  - Object:

    * host object: implementation-dependent

    * object that implements Call: "function"

    * otherwise: "object" (WTFJS_)

- For undeclared variable, typeof operation 的结果是 "undefined" (WTFJS_).
  注意这不同于直接作为 rvalue 使用时的结果, 那时 raise ReferenceError.

  这可用于检查某个 identifier 是否定义, 而不导致 raise exception. 所以还是
  有用的. 其实需要使用这种办法还是因为 js 中缺乏更合理的处理机制. 一个合理
  设计的语言中的合理代码根本不该出现不知道某个量是否存在这种情况的.

.. [1] In the first implementation of JavaScript, JavaScript values were
       represented as a type tag and a value, with the type tag for objects being 0,
       and null was represented as the NULL pointer (0x00 on most platforms). As a
       result, null had 0 as a type tag, hence the bogus typeof return value.

void
^^^^
evaluates the given expression and then returns ``undefined``.

delete
^^^^^^
::

  delete object.property
  delete object['<property>']

- delete operator removes a property from an object (including arrays).
  Unlike in python, it can not be used to remove arbitrary local identifier.

  Global identifiers are essentially properties of global object. But,
  identifiers declared with ``var``, ``let``, ``const`` etc. become
  non-configurable properties. Only implicitly global identifiers are
  configurable. But since implicitly global identifiers are discouraged,
  ``delete`` operator is essentially only useful for ``object.property``
  form.::

    var x = 1;
    Object.getOwnPropertyDescriptor(global, 'x'); // ... configurable: false
    delete x; // false or TypeError
    y = 1;
    Object.getOwnPropertyDescriptor(global, 'y'); // ... configurable: true
    delete y; // true but not even possible in strict mode.

- Return true for all cases except when the property is an own non-configurable
  property, in which case, false is returned in non-strict mode, as deletion
  is unsuccessful.

- delete only has an effect on own properties.

- In strict mode, if delete is used on a direct reference to a variable, a
  function argument or a function name, it will throw a SyntaxError.

equality operators
------------------

- ``===`` vs ``==``. when use which?

  when you want to allow certain degree of fuzziness in equality checking, use ``==``,
  otherwise if you wanna restrict allowed values, use ``===``.

  In other words, when you really know what you are doing (by understanding every possible
  cases that may occur as your operands), you may use ``==``; othwerwise stick to ``==``.

equality comparison
^^^^^^^^^^^^^^^^^^^
::

  == !=

- loose equality.

- type coercion is allowed under the hood (WTFJS_).

- logic:

  * if both types are the same, perform strict equality comparison.

  * coerce one or both values to a different type until the types match, where
    then a simple value equality can be checked.

strict equality comparison
^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  === !==

- strict equality.

- type coercion is not allowed.

- When both types are the same:

  * if both are objects, comparisons will simply check whether the references
    match, not anything about the underlying values.

relational operators
--------------------
::

  < > <= >=

- type coercion is allowed (WTFJS_).

- logic.

  * objects are firstly converted to primitive values.

  * if both are strings, they are compared lexicographically.

  * if at least one of both is not string, they are coerced to numbers
    then compared.


in operator
-----------
::

  <prop> in <obj>

- ``in`` operator tests whether a property name is reachable from an object.
  This includes an object's own property and traversing its prototype chain.

- RHS of in operator must be an object.

- 目前没有 builtin 方法可以获取一个 object 的所有 properties, 包含 own properties,
  inherited properties, enumerable and non-enumerable. 即 in operator test 的
  property set. 必须手动遍历所有父类, 对每个类 ``getOwnPropertyNames``.

instanceof operator
-------------------
::

  obj instanceof cls

- test whether the ``prototype`` property of a class/constructor function
  appears anywhere in the prototype chain of an object.

- to test whether an object appears in another object's prototype chain,
  use ``.isPrototypeOf()`` method.

- 注意, 在 JS 中, instanceof 和 typoeof 两个 operator 检查的是完全不同的东西,
  不具有相关性. 前者检查的是 prototype chain 的相关问题; 后者检查的是一个数据
  值的所属几种基本类型. (WTFJS_)

assignment operators
---------------------
assignments are operators. thus assignment is an expression, unlike python.

conditional operator
--------------------
::

  <boolean-expression> ? <expr1> : <expr2>

spread and rest syntax
----------------------
::

  ...<iterable>

- Spread syntax allows an iterable to be expanded in places where zero or more
  arguments (for function calls) or elements (for array literals) are expected,
  or an object expression to be expanded in places where zero or more key-value
  pairs (for object literals) are expected.

- spread syntax can be used as:

  * the rest parameter of the parameter list of function definition. 表示 0 or
    more remaining arguments.  此时, rest parameter 必须是最后一个参数. 在
    function call 中, 该参数收集到 an array of remaining arguments.

    注意, 在函数定义中出现的 spread syntax 仍然可以一般性以多层形式出现.::

      function f(a, ...[b, c, ...d]) {
          //
      }

    这与 python 不同.

  * an argument of the argument list of function call. operand must be an iterable.
    iterable 生成的所有值, 成为 argument list 的一部分. spread syntax 可以在 argument
    list 中出现多次, 且位置不限.

  * in array literal. 进行 iterable unpacking. unpacked elements 成为新 array 的成员.
    spread syntax 可以出现多次, 且位置不限.

  * in object literal. 进行 mapping unpacking. unpacked key-value pairs 成为新的 object
    的属性和值. 可以出现多次, 且位置不限.::

      {...{a:1}, b:2, ...{c:3}}

  * in LHS of destructuring assignment. 收集 0 个或多个 remaining RHS's
    elements at the same unpacking level. 注意 reset parameter 必须是同层
    的最后一个项. 并且支持 nested spread syntax.::

      let [a,b, ...c] = [1,2,3,4]
      let [a,b, ...[c, d, ...e]] = [1,2,3,4,5,6]
      let a,b;
      ({a, b, ...c} = {c:10, d:20, e:30, f:40}); //c: {e:30, f:40}

    object destructure 似乎不支持 nested.

function expressions
--------------------
Including simple function expressions, property accessor function, arrow function
expression, See `function`_.

function
========

function statements
-------------------

See `function`_.

function declaration statement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  function <identifier> ([param=default, ...]) {
      [statements]
  }

- function declaration creates a lexical scope. (a function scope.)

- ``var`` declarations in function has function scope.

  ``var`` + function scope is fine enough for normal programming requirements.
  That's almost all we have in Python.

- hoisting. Wherever a function declaration is inside a scope, that declaration
  is taken to belong to the entire scope and accessible everywhere throughout
  (WTFJS_).

  Function variable and function definition is hoisted together. This is
  different from ``var`` hoisting.

  Function declaration is hoisted before ``var`` declaration. For duplicate
  function declarations, the latter override the former.

  Note that function expression does not hoist of course. The following code
  may trick you::

    func(); // `TypeError`, NOT `ReferenceError`. As `func` is hoisted.
    var func = function func() {
        ...
    }

- Special note on block-level function declaration (ES6) [SOBLKFUNC]_ (WTFJS_).

  * In strict mode, function declared in block scope is hoisted in the scope,
    and only visible inside the block scope. Reference the same identifier
    outside of defining scope raises ``ReferenceError``.::

      "use strict";
      foo(); //ReferenceError
      if (true) {
         function foo() { console.log( "a" ); }
      }
      else {
         function foo() { console.log( "b" ); }
      }
      foo(); //ReferenceError

  * In non-strict mode, function identifier is hoisted to the nearest function
    or global scope, but function definition is not visible until declaration
    statement is reached. After that, the definition is visible until the end
    of nearst function or global scope.::

      /* var foo; */ // implicit hoisting.
      foo(); // TypeError
      if (true) {
         function foo() { console.log( "a" ); }
      }
      else {
         function foo() { console.log( "b" ); }
      }
      foo(); // a

- When function is called, its formal parameters are set values sequentially
  corresponding to argument list. All remaining formal parameters fall back to
  their default values. If ``default`` is unspecified, it's ``undefined``.

- 模拟更灵活的 keyword parameter.

  注意 ``param=default`` 形式的参数定义, 在 JS 中只是 explicitly 设置了参数的
  默认值, 并没有允许 keyword 形式的参数赋值. 函数在调用时, 参数传递仍然是
  positional 依次赋值的.

  使用 object destructuring assignment 可以模拟 keyword argument 形式参数赋值.

- Differing from variable declaration with initial value, function declaration
  is handled entirely by compiler: compiler handles both the function name
  declaration in scope and function body definition during code-generation.

- JS 中, 由于 ``this`` 是根据调用情况自动赋值的, 一个函数本身可以既做单纯的
  函数来使用, 也可以作为 object bound method 使用. 而如果要作为 class unbound
  method 使用, 需要使用 ``Function.prototype.call()``, ``Function.prototype.apply()``.

generator function declaration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  function* name([param[, ...]]) {
      // statements
  }

- generator function can not be used as constructor. (注意 generator function
  与 normal function 只是语法上长得像, 实际上是在执行逻辑上完全不同的.)

function expressions
--------------------

See `function`_.

function expression
^^^^^^^^^^^^^^^^^^^
only issues specific function expression is recorded here.
For all other aspects and descriptions refer to `function declaration statement`_
section.

- ``function`` keyword can be used to define a function expression inside
  another expression.

- function name. You should always provide a name to your function expression.
  [SOnamedFuncExp1]_ [SOnamedFuncExp2]_

  * function name is local to function body::

      let func = function func() {
        ...
      }
      // equivalent to
      let func = function () {
        var func = // some kind of self reference
      }

  * function name is required if function is recursive, i.e. it needs to call
    itself inside function body.

  * function name is required when an event handler function wants to unbind itself
    after it fires.

  * anonymous function:
    If function name is omitted in function expression, it is inferred based on
    defining context, e.g., used as RHS of assignment, as object property value,
    etc., which eventually becomes ``function.name`` attribute. If not inferred,
    ``function.name`` is ``""``, which is anonymous function.

    Some hard disadvantages of anonymous function:

    - debugging: less informative and hard to identify in call stack.

    - recursion: self-referencing in function body is not possible. Thus recursion
      is impossible.

  * named function can be seen in stack traces, call stacks, list of breakpoints, etc.

  * Even if name is not required, sometimes it helps to document your intent, e.g.::

      some_operation_with_callback(function success() {...}, function failed() {...})

  * if function expression is used for assignment, name is not very useful::

      let foo = function () {...};

    But why needs assignment anyway? Just use function declaration statement is fine
    enough::

      function foo() {
          ...
      }

- Immediately invoked function expression (IIFE)::

    (function IIFE() {
        ...
    })();

  or::

    (function IIFE() {
        ...
    }())

  The outer ``(...)`` that surrounds IIFE is needed to prevent it from being
  treated as a function declaration statement.

  IIFE is often used as a purely executed chunk of code, to prevent polluting
  global namespace. Many libraries use this trick.

property accessor function
^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  get <prop>() { ... }
  get [<expression>]() { ... }

  set <prop>(value) { ... }
  set [<expression>](value) { ... }

arrow function expression
^^^^^^^^^^^^^^^^^^^^^^^^^

- In arrow functions, ``this`` retains the value of the enclosing
  lexical scope's ``this``. No matter what happens.

  但是注意, 如果 enclosing lexical scope 的 ``this`` is dependent on call-site.
  则 arrow function's ``this`` is fixed at enclosing function's call-site.::

    function f() {
        return () => {
            console.log(this.a);
        };
    }

    var x = {
        a: 1
    }, a = 2;

    f.call(x)();
    f()();

- arrow function is very useful for callbacks. because of its succinctness and
  lexical ``this`` behavior.

class
=====

- In JS, classes are just special functions.

  * ``new <func>(<args>)`` creates instances of ``func`` class.

  * ``func`` itself serves as the constructor of class.

  * ES6 ``class`` syntax is just a syntactic sugar. It does not change the way
    class works in JS.

- 与正常的 OOP 语言不同, JS 中不存在明确的 class 与 instance 的区分. 一个 object
  是根据某个类 object 的 prototype 生成的. 这个 object 本身还可以作为类去实例化
  prototype 部分.

- Inheritance in JS.

  * JS uses a prototype-based inheritance. 与正常的 OOP language 不同, 在 JS
    中, 一个 object 具有它自己的部分, 和它的作为 class 的部分 (即 ``prototype``
    object). 只有 prototype 部分是实例的模板, 而它自己的部分实例是访问不到的.

  * JS doesn't support multiple inheritance.

- Polymorphism in JS.

  * before ES6, 对于一个父类的方法, 子类只有两个选择: 完全继承或完全覆盖. 子类
    方法中, 没有机制能够相对地引用父类同名方法. 除非直接明确访问父类获取所需
    方法再 ``.call(this)`` bind 至本实例. 然而这种写死类名的方式维护成本太高.

  * In ES6 and later, class syntax solved super method reference problem.

class definition
----------------

pre-ES6
^^^^^^^
- definition function used as constructor call. If there is parent class,
  their constructors must be called::

    function Cls(<args>) {
        // call parent class constructors
        Parent.call(this, <args>);
        // initialization logics
    }

- If there is parent class, link ``Cls.prototype`` to parent class's
  prototype.::

    Cls.prototype = Object.create(Parent.prototype);
    // or ES6 and later
    Object.setPrototypeOf(Cls.prototype, Parent.prototype);

  注意, 使用以下代码对 prototype 赋值是不合适的::

    Cls.prototype = new Parent();

  因为对 Parent class 实例化会执行 Parent constructor, 这样就执行了很多不必要
  的逻辑, 可能有 unwanted side-effect, 而且这里如果需要传递参数进去也会很奇怪.

- If another mixin class is needed::

    Object.assign(Cls.prototype, Parent2.prototype);

- fix constructor attribute if so inclined::

    Cls.prototype.constructor = Cls

- define class attributes and instance methods::

    Cls.prototype.attr = val;
    Cls.prototype.meth = function meth(args) {
        // ...
    }

  如果子类要 override 父类的同名方法, 并在其中调用 overridden 方法, 唯一的方式
  就是使用 absolute name::

    Parent.prototype.meth.call(this, <args>);

ES6 and after
^^^^^^^^^^^^^

class declaration statements
""""""""""""""""""""""""""""
::

  class <name> [extends <parent>] {
      // body
  }

- inheritance.

  * to inherit a parent class, use ``extends`` keyword. Class-declared classes,
    function-declared classes, and builtin classes can all be extended this
    way.

  * Use ``super`` keyword to access data properties and methods at higher
    prototype chain. In constructor method, use ``super(<args>)`` to call
    parent class's constructor.

- method definition.

  * only methods but not variables can be defined in class definition block.
    Methods can be defined using concise method definition syntax and concise
    accessor property definition syntax.

  * To define a static method, use ``static`` keyword.

    注意到在 static method 中, ``this`` keyword 一般指向 class 本身 (仍然是
    基于 `this keyword`_ rules). 因此可以访问 class function 上的一切属性.

  * To define an instance method, just define it without ``static``.

    在 instance method 中, ``this`` keyword 一般指向 instance object.

  * constructor is defined obviously using ``constructor`` method.  There can
    only be one constructor method in class definition body. Otherwise
    SyntaxError is raised.

    Default Constructor method does nothing.

- data properties.

  * Class-only data properties and class data properties has to be defined
    outside of class definition body.::

      class A {}
      A.x = 1;
      A.prototype.b = 2;

- mixin classes. 由于 JS 不支持多继承, mixin class 必须通过 factory function,
  在使用时再生成, 作为 main base class 的子类. 从而在 prototype chain 中
  插入自己的方法或 override 父类的方法.::

    let mixin_factory = Base => class SomeMixin extends Base {
        // mixin methods
    }

    // in use
    class Child extends mixin_factory(Parent) {
        // methods
    }

- Definition interpretation. ES6 class syntax 与 pre-ES6 的 function syntax
  生成的是相同的东西. 具体讲,

  * 生成的 class object 本身是一个 constructor function, 由 constructor
    method definition 决定.

  * ``static`` keyword 生成的 static method 即 class object 的 properties.

  * 其他所有 methods 成为 ``cls.prototype`` object 的 properties.

  * 对于 ``extends Parent``, 包含两个 prototype link. ``Child`` linked to
    ``Parent``, 以及 ``Child.prototype`` linked to ``Parent.prototype``.

- hoisting. class declarations are *not* hoisted like function declarations.
  So classes must be lexically defined before they are used.

- An identifier defined using class syntax can not be redefined.

- The whole class body is executed in strict mode.

- class syntax 定义的 class function 只能在实例化时与 ``new`` 一起使用.
  Otherwise TypeError is raised.

class expression
""""""""""""""""

This section shows stuffs specific to class expression. For other info, see
`class declaration statements`_.

- class expression can be named or unamed. The class name in class expression
  is local to class body.

- Anonymous class shares the same problems with anonymous function expression.

static keyword
""""""""""""""
- define static method for a class.

- those static methods are only available on class function object.

- Based on normal ``this`` value resolution rules, a static method can access
  another static method in its body.

- 在 JS 中不存在正常的 class method 语法. ``static`` 同时可以用于定义传统意义上
  的 static method 和 class method. 例如创建 utility functions, alternative
  constructor 等.

super keyword
""""""""""""""
::

  super(<args>)
  super.prop

- super keyword is used to access an object's parent.

- super bindings.

  - In constructor method, ``super`` must be called as a function, it represents
    the parent class's constructor.

  - In instance method, ``super`` represents the parent prototype object. Thus
    have access to all prototype's properties. But ``super`` can not be used
    alone here (meaning without property reference operation).

  - In static method, ``super`` represents the parent class function object. Thus
    have access to parent's static methods (or class methods). But ``super``
    can not be used alone here (meaning without property reference operation).

- super keyword can't be used for deleting properites on parent prototype.::

    delete super.prop; // ReferenceError

- super bindings are static, they don't change at different call-site. They
  are bound at definition time.::

    class P {
        foo() { console.log( "P.foo" ); }
    }

    class C extends P {
        foo() {
            super();
        }
    }

    var c1 = new C();
    c1.foo(); // "P.foo"

    var D = {
        foo: function() { console.log( "D.foo" ); }
    };

    var E = {
        foo: C.prototype.foo
    };

    // Link E to D for delegation
    Object.setPrototypeOf( E, D );

    E.foo(); // "P.foo"

extends keyword
""""""""""""""""
::

  class Child extends Parent {}

- to extend a class.

- Child extends Parent 时, 做了两方面的 linking.

  * ``Child.prototype`` is prototype-linked to ``Parent.prototype``.
    Namely,::

      Object.getPrototype(Child.prototype) === Parent.prototype

    这样, instance method and traditional class properties can be delegated to
    parent class prototype.

  * ``Child`` class function object is prototype-linked to ``Parent``
    class function. Namely,::

      Object.getPrototypeOf(Child) === Parent

    这样, static methods (including class methods) and static properties
    can be delegated to parent class function object.

- A class can extend another class or null. 当继承 null 时, 等价于::

    Child.prototype = Object.create(null);

  这样, Child 不包含任何默认继承自 ``Object.prototype`` 的属性.

constructor method
""""""""""""""""""
- constructor method 生成的就是 class function.

- There can be only one special method with the name "constructor" in a class.
  Otherwise SyntaxError is raised.

- The default constructor does nothing.::

    constructor() {}

  For derived class, the parent class's constructor is inherited by default.

instantiation
-------------
- Instance object is created by ``new Func(<args>)`` operation. See
  `new operator`_.

prototype
---------
- All functions by default has a public, non-enumerable ``prototype`` property,
  which is a reference to an arbitrary object.

- Prototype is denoted by ``[[Prototype]]`` in spec.

- An object's ``prototype`` property is NOT *the* object's prototype, but the
  prototype of the object's *instances*. The object itself's prototype is only
  accessible via ``Object.getPrototypeOf()``.

prototype chain
^^^^^^^^^^^^^^^

- A object has a prototype chain linked to its parent classes. This prototype
  chain is internal, but directly accessible like in python (``__mro__``). but
  can be inspected indirectly via ``Object.getPrototypeOf()``.

- There two ways to create a new object that links to a specified prototype
  object.

  * as a side-effect of ``obj = new Func(<args>)`` instantiation, which
    cause obj linked to ``Func.prototype``.

  * as a direct operation of ``obj = Object.create(<proto>)``, which cause
    obj linked to proto.

method resolution
-----------------

property reference
^^^^^^^^^^^^^^^^^^

- ``[[Get]]`` internal method is called to get a property of a object.

- logic of ``[[Get]]``.

  * Check whether the property is the object's own property.

  * Check whether it's the object's prototype's own property.

  * Check the prototype of the object's prototype object... doing so
    recursively upwards, until reaching ``Object.prototype``.

  * If not found anywhere, return undefined.

property assignment
^^^^^^^^^^^^^^^^^^^

- ``[[Set]]`` internal method is called to set a property.

- ``[[Set]]`` is invoked when explicit assignment operations (including ++, --
  operators), but not invoked when using ``Object.defineProperty`` etc.

- logic of setting ``prop`` to ``value``, on ``obj``. e.g, ``obj.prop = val``.

  * If ``prop`` not found anywhere (as own properties and on prototype chain),
    it's created as a data descriptor on obj.

  * If ``prop`` is found as a writable data descriptor anywhere, obj's own
    ``prop`` is modified or created as appropriate.

  * If ``prop`` is found but a readonly data descriptor anywhere, assignment is
    disallowed and ignored in non-strict mode. Error is raised if in strict
    mode.

  * If ``prop`` is found as a accessor descriptor anywhere, setter is invoked.

- Be very careful that ``[[Set]]`` is invoked for ``++``, ``--`` operators.
  This may cause unexpected behavior::

    function A() {}
    A.prototype.a = 1;
    function B() {}
    B.prototype = new A();
    let b = new B();
    b.a++;
    console.log(b.a, B.prototype.a);

type introspection
------------------

Three ways to inspect the type and prototype of an object, see their
respective sections for detail.

- Object.getPrototypeOf

- Object.prototype.isPrototypeOf

- instanceof

OLOO -- an alternative design
-----------------------------

- OLOO: Objects Linked to Other Objects.

- OLOO design ditches class design patterns (which is not very well supported
  in js), embraces purely prototype chain and behavior delegation.

- Some design notes:

  * See objects in prototype chains are peers rather than parent-child
    relationship, where one object delegates some of its operations to another
    object.

  * Avoid naming things the same at different levels of the prototype chain.
    This is different from polymorphism in OOP design.

definition
^^^^^^^^^^

- Create base object, note it's not creating base class. It's just normal object
  used as upper node in prototype chain, used for delegation. We are not creating
  classes.::

    let Parent = {
        attr: ...,
        init: function ...,
        meth: function ...,
    }

  Both class attribute and instance methods are defined here.
  Constructor/initializer must be defined manually.

- Create derived object, linked to parent.::

    let Child = Object.create(Parent);

- Create child's methods etc.::

    Child.meth = ...;

- To make instance::

    let c = Object.create(Child);

modules
=======

historical notes
----------------
There are two kinds of JS modules:

- ES5 module pattern: Before ES6, JS language has no builtin module mechanism
  (WTFJS_).  Using function and closure to emulate lousy module/class
  interface. These are standardized by AMD, CommonJS and UMD libraries. See
  `modules <modules.rst>`_.

- ES6 builtin module syntax.

The most important difference between the two is that:

* module pattern is a hack that works well. They are essentially normal objects,
  functions with closures and so forth. They just looks like modules or
  classes. They works like module/class (rather than normal objects/functions)
  only at runtime. For compiler, they are not any special than other functions,
  objects. In other words, the "module/class" semantics 是由程序员赋予的, 并且
  只在 runtime 存在.

* ES6 module syntax is defined at language level and implemented by interpreter.
  The semantics is recognized by compiler at compile-time. Compiler is responsible
  to perform necessary checks/optimizations and throw early errors if one exists.

Here we focus on ES6 modules.

overview
--------

- Each JS source file is a module.

- Each module can import another module entirely or only individual members of it.

- Each module can export a set of public APIs that is importable by other modules.


built-in objects
================

built-in functions
------------------

eval()
^^^^^^
take JS code in string and execute it at current runtime execution point.  Code
can contain an expression or a suite of statements.  Return value is the return
value of executed JS code::

  eval('2+2') -> 4
  eval('var x = 1;') -> undefined

Disadvantages:

- makes JS code slow.

  * it has to invoke the JS interpreter.

  * modern javascript interpreters convert javascript to machine code. This
    means that any concept of variable naming gets obliterated. Thus, any use
    of eval will force the browser to do long expensive variable name lookups
    to figure out where the variable exists in the machine code and set it's
    value. Additonally, new things can be introduced to that variable through
    eval() such as changing the type of that variable, forcing the browser to
    reevaluate all of the generated machine code to compensate.

- security risk.

In strict mode, ``eval()`` is executed in its own lexical scope, which makes it
impossible to modify program's lexical scope. In this case, only ``eval()``
program logic's side effect and its return value have impact on calling program.

built-in exceptions
-------------------
- RangeError

  * semantics: invalid value as an argument to a function that does not allow a
    range that includes the value.

  * builtin function that throws:

    - String.prototype.normalize()

    - Number.prototpye.toExponential()

    - Number.prototpye.toFixed()

    - Number.prototpye.toPrecision()

- ReferenceError.

  * semantics: nonexistent identifier is used as rvalue.

- SyntaxError

  * semantics: JavaScript compiler/engine encounters tokens that does not
    conform to the syntax of the language when parsing code.

- TypeError

  * semantics: when an operand or argument passed to a function is incompatible
    with the type expected by that operator or function.

- URIError

  * semantics: when the global URI handling functions are passed a malformed
    URI.

compilation
===========
- modern JS interpreters convert JS code to machine code (JIT) during execution.

Execution model
===============

- code execution is managed by javascript runtime engine. It is distinct from
  js compiler.

Scope
-----
- JS use lexical scope.
  lexical scope rule: code in one scope can access identifiers of either that
  scope or any scope outside of it. This includes both lvalue & rvalue
  resolution.

  * For rvalue, if an identifier is not found, ``ReferenceError`` exception is
    raised, except when it is used as operand of ``typeof`` operator.

  * For lvalue, if a variable could not be found by traversing nested scope until
    global scope, it will be created in global scope. DON'T DO IT.

    Unless in strict mode, this will raise ``ReferenceError``.

- An identifier defined in inner scope shadows the identifier of the same name
  defined in the outer scope.

- Global scope is represented by global object. In browser, it's ``window``. In
  nodejs, it's ``global``.

- lexical scope and iteration statements. Iteraction statements typically contains
  a block scope (with block statement). The point is that for every loop iteration,
  a different lexical block scope is created. 这对于 closure 非常重要, 当一个函数
  的执行涉及 closure over loop-created lexical scope 时, 它只能访问函数定义时对应
  的 iteration 的 block scope.

  Compare::

    for (var i=1; i<=5; i++) {
        setTimeout( function timer(){
            console.log( i );
        }, i*1000 );
    }

    for (var i=1; i<=5; i++) {
        let j = i;
        setTimeout( function timer(){
            console.log( j );
        }, j*1000 );
    }

    for (var i=1; i<=5; i++) {
        (function(j){
            setTimeout( function timer(){
                console.log( j );
            }, j*1000 );
        })( i );
    }

- There are two ways lexical scope can be modified at runtime:

  * ``eval()``, ``setInterval()``, ``setTimeout()``, ``new Function()`` etc.
    that can execute program text at runtime.

  * ``with`` statement, which is deprecated.

Closure
^^^^^^^
- definition.
  A function is able to remember and access its lexical scope even
  when that function is executing outside its lexical scope. The function's
  reference to its defining lexical scope is called closure. In other words,
  a function has closure over its lexical scope.

- Here the aforementioned lexical scope might be some outer function scope, or
  even global scope.  As long as when the function is executing outside of its
  original defining scope, closure happens. For closure over global scope, it
  happens when the function is executed outside of its defining module.

  A function's reference to its outer lexical scope, prevents the scope's memory
  and whatnot being GC-ed.

strict mode
===========
- pragma::

    "use strict";

  can be used in a function scope or global scope.

- ``"use strict";`` pragma must be the first statement in a specific
  lexical scope, and it is effective until the end of the specified
  scope.

- The pragma conforms lexical scope rule. In other words, whether a
  piece of code runs in strict mode depends on whether its lexical
  scope is in strict mode.::

    function foo() {
        console.log( this.a ); // non-strict mode
    }

    var a = 2;

    (function(){
        "use strict";

        foo(); // strict mode
    })();
    // prints: 2

- keeping the code to a safer and more appropriate set of guidelines.

- generally more optimizable by the engine.

- it should be used for all your codes and declared at the top of source
  file.

security
========
- 在比较老的浏览器中, 存在 JSON array 带来的 vulnerability.

  原理是, 使用 ``<script src="">`` tag 获取一个 json response,
  这个 json 是 array, 浏览器会当作 js array 去构建这个元素.
  若在其他 script 部分, 对 Array 进行了部分重定义, 则可以截取
  到 json array response 的内容. 因此, 推荐做法是 json response
  顶层一定要是 {}, 不能是 [].

  注意这种执行行为在 ES5 中已经被禁止了, 这个漏洞和 workaround
  不再必要.

weird designs
=============
.. _WTFJS:

WTFJS-related weird language designs are labeled WTFJS.

javascript core features
========================
- "object"-oriented (prototype-based).

- event-driven architecture and asynchronous processing.

references
==========
.. [SOnamedFuncExp1] `Why use named function expressions? <https://stackoverflow.com/a/15336541/1602266>`_
.. [SOnamedFuncExp2] `What is the point of using a named function expression? <https://stackoverflow.com/questions/19303923/what-is-the-point-of-using-a-named-function-expression>`_
.. [SOBLKFUNC] `What are the precise semantics of block-level functions in ES6? <https://stackoverflow.com/questions/31419897/what-are-the-precise-semantics-of-block-level-functions-in-es6>`_
.. [SOLetLoop] `let keyword in the for loop <https://stackoverflow.com/questions/16473350/let-keyword-in-the-for-loop>`_
.. [WellKnownSymbols] `Detailed overview of well-known symbols <https://dmitripavlutin.com/detailed-overview-of-well-known-symbols/#6speciestocreatederivedobjects>`_
.. [SOArrayLike] `javascript - Difference between Array and Array-like object <https://stackoverflow.com/questions/29707568/javascript-difference-between-array-and-array-like-object>`_
.. [SOJSAutobox] `Does javascript autobox? <https://stackoverflow.com/questions/17216847/does-javascript-autobox>`_
.. [SOJSRESticky] `What is the purpose of the 'y' sticky pattern modifier in JavaScript RegExps? <https://stackoverflow.com/questions/30291436/what-is-the-purpose-of-the-y-sticky-pattern-modifier-in-javascript-regexps>`_
