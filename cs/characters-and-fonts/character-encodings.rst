character set
=============

- A character set consists of a character repertoire and their encodings.

- The repertoire of a character set is the collection of characters in the set.

- Encodings is a map from character symbols to numerical representations.

collation
=========

- A collation is a set of rules for comparing characters in a character set.
  一个 character set 可以有多个 collation.

- binary collation: the order of characters in a character set is determined
  solely by comparing their encodings.

- case-insensitive collation: uppercase and lowercase characters are compared
  equal.

Unicode
=======

characters
----------

- In unicode, each character is identified by an unique name and integer number
  pair. The number representing a character is its code point.

planes
------

- A character plane is any of ``xy0000 - xyFFFF``, which contains 2**16 chars
  in total. There are currently 17 planes.

- Basic Multilingual Plane (BMP): U+0000 - U+FFFF

  * ASCII: U+0000 - U+007F.

- supplementary planes: U+10000 - U+10FFFF. So there are the 16 supplementary
  planes.
