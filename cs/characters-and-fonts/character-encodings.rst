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

- ASCII: U+0000 - U+007F.

- Basic Multilingual Plane (BMP): U+0000 - U+FFFF

- supplementary characters: U+10000 - U+10FFFF
