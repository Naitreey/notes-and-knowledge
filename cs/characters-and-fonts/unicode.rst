Unicode
=======
overview
--------
- The Unicode standard is a standard for consistent handling of text expressed
  in most of the world's writing systems.

characters
----------

- In unicode, each character is identified by an unique name and integer number
  pair. The number representing a character is its code point.

UCS and ISO/IEC 10646
=====================
- The international standard ISO 10646 defines the Universal Character Set
  (UCS).

- UCS is a superset of all other character set standards. It guarantees
  round-trip compatibility to other character sets, meaning that no information
  is lost if you convert any text string to UCS and then back to its original
  charset.

coverage
--------
- most of modern and historic scripts.
 
- graphical, typographical, mathematical and scientific symbols.
 
- emoji.

planes
------
- UCS planes: A UCS plane is a subset of 2**16 characters in the 31-bit UCS
  character set. In other words, any of ``xy0000 - xyFFFF``.
  
- Basic Multilingual Plane (BMP), Plane 0.
  
  * U+0000 - U+FFFF.

  * includes the most commonly used characters and all characters in older
    encoding standards.

  * ASCII: U+0000 - U+007F.

  * ISO 8859-1/Latin-1: U+0000 - U+00FF.

- Current plans are that there will never be characters assigned outside the
  21-bit code space from 0x000000 to 0x10FFFF. In total, these are currently 17
  planes.

  * BMP.

  * supplementary planes: U+10000 - U+10FFFF. 16 个.

characters
----------
- A UCS/Unicode character has:

  * a code point

  * an official name.

- Representation: ``U+<hex-code-point>``

relation with Unicode
---------------------
- The Unicode standard is in sync with ISO/IEC 10646.

UTF-8
=====
- UTF-8 is a character encoding of the Unicode character set.

- With the UTF-8 encoding, Unicode can be used in a convenient and backwards
  compatible way in environments that were designed entirely around ASCII
  (because code points are encoded with variable width), like traditional Unix.
  UTF-8 is the way in which Unicode is used under Unix, Linux, and similar
  systems.
