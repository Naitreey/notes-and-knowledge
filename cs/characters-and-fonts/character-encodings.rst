character set
=============

terms
-----

- character: A character is a minimal unit of text.

- character set: A character set is a collection of characters defined by a
  defining purpose.

- coded character set (CCS): a function that maps characters to code points (each
  code point represents one character).

- character repertoire: a full set of abstract characters in a character set.

- code point: A code point is a number corresponding to a character in
  a coded character set.

character encoding
==================

terms
-----
- character encoding scheme (CES): A mapping of code points to code units to
  facilitate storage in a system that represents numbers as bit sequences of
  fixed length (serialization).
  
  如果不局限于 computing, an encoding can be any system that is used to
  represent the repertoire of a character set in a specific form. In general,
  it encodes code points into some kind of "form", depending on the specific
  field of application. E.g., in signal processing, a character encoding
  encodes code points into electrical plulses.

- code unit: A code unit is a bit sequence used to encode each character of
  a repertoire within a given character encoding.

  For example, A code unit in US-ASCII consists of 7 bits; A code unit in
  UTF-8, EBCDIC and GB18030 consists of 8 bits; A code unit in UTF-16 consists
  of 16 bits; A code unit in UTF-32 consists of 32 bits.

- code page: A historical term that usually means a byte-oriented encoding.

collation
=========

- A collation is a set of rules for comparing characters in a character set.
  一个 character set 可以有多个 collation.

- binary collation: the order of characters in a character set is determined
  solely by comparing their encodings.

- case-insensitive collation: uppercase and lowercase characters are compared
  equal.
