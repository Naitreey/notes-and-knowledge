Unicode
=======
overview
--------
- The Unicode standard is a standard for consistent handling of text expressed
  in most of the world's writing systems.

encoding model
--------------
Unicode and ISO 10646 标准构建出了一个三层的映射体系. 这三层分别是 character
repertoire, coded character set, character encoding schemes.

抽象字符通过 coded character set 映射为 code point, code point 通过 character
encoding scheme 映射为二进制表达形式.

The purpose of this decomposition is to establish a universal set of characters
that can be encoded in a variety of ways.

versions
--------
- version 1.0.0 (1991)

- version 11.0 (2018)

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
  
- RFC 3629 defines that there will never be characters assigned outside the
  21-bit code space from 0x000000 to 0x10FFFF. An anything outside of this
  range is invalid unicode code point. In total, these are currently 17 planes.

  - Basic Multilingual Plane (BMP), Plane 0.
    
    * U+0000 - U+FFFF. For each char, normally represented by ``U+XXXX``.
  
    * includes the most commonly used characters and all characters in older
      encoding standards.
  
    * ASCII: U+0000 - U+007F.
  
    * ISO 8859-1/Latin-1: U+0000 - U+00FF.
  
  - supplementary planes.
    
    * U+10000 - U+10FFFF. 16 个.
      
    * For each char, normally represented by ``U+XXXXXX``.

- All code points in the BMP are accessed as a single code unit in UTF-16
  encoding and can be encoded in one, two or three bytes in UTF-8. Code points
  in Planes 1 through 16 (supplementary planes) are accessed as surrogate pairs
  in UTF-16 and encoded in four bytes in UTF-8.

characters
----------
- A UCS/Unicode character has:

  * a code point

  * an official name.

- Representation: ``U+<hex-code-point>``

- combining character. A combining character is not a full character by itself.
  It is an accent or other diacritical mark that is added to the previous
  character. The combining-character mechanism allows one to add accents and
  other diacritical marks to any character.

- precomposed character. The most important accented characters, like those
  used in the orthographies of common languages, have codes of their own in UCS
  to ensure backwards compatibility with older character sets. 

special characters
^^^^^^^^^^^^^^^^^^
- replacement character (U+FFFD): �. used to replace an unknown, unrecognized
  or unrepresentable character

relation with Unicode
---------------------
- The Unicode standard and ISO/IEC 10646 are two different standards published
  by different organizations that essentially defines the same character set.
  Their code tables are always in sync.

- ISO 10646 is not much more than a simple character set table, an extension of
  previous standards like ISO 8859. In contrast, Unicode adds rules for
  collation, normalization of forms, and the bidirectional algorithm for
  right-to-left scripts such as Arabic and Hebrew, etc.

Encodings
=========
- UTF-16 and UTF-32 是最自然的 unicode encoding. 这是因为 unicode charset is 
  31-bit. 每个 plane 是 16-bit. 所以 code unit 选择为 16bit or 32bit 都是比较
  合适的.

- 当 code unit 由多个 bytes 构成时, 一般具有 BE & LE 两种, 适用于两个类型的
  CPU. UTF-16 and UTF-32 就是这样. BE & LE 的区别是, 一个 code unit 中各个 byte
  的高低位排列顺序.

- naming of UTF-8, UTF-16, UTF-32:

  * UTF: Unicode Transformation Format

  * N: code unit bit size.

UTF-8
-----

- UTF-8 is a character encoding of the Unicode character set.

- UTF-8 中每个 code unit 由 1 byte 组成.

- It's a variable-width encoding, meaning for each unicode code point,
  the length of encoded byte sequence is variable.

- Usage:

  * UTF-8 是使用最广泛的 Unicode 编码形式, 其最主要的应用在于 serialize unicode
    data to storage, to network 等需要 binary 序列化的场景下.

scheme
^^^^^^
- ASCII subset (U+0000 to U+007F) are encoded by 1 byte, from 0x00 to 0x7F.
  This is identical to ASCII encoding.

- ASCII 之外的字符 are encoded as a sequence of several bytes, 其中的每个 byte
  has the most significant bit set. 这样的意义是两点:

  * 避免任何一个 byte 是 null char.

  * 由于 ASCII 以外字符的编码保证每个 code unit 最高位都是 1, 这样合法的
    multibyte encoding 中不会包含任何与 ASCII 相同的 byte subsequence. 这样限制
    的目的是, 如果一个程序本身不支持 utf-8, 只支持 ascii, 也能 safely process
    utf-8 encoded text. 不会错将一个 multibyte 编码的字符看作是多个 ascii.

- The first byte of encoding of a non-ASCII character is always in the range of
  0xC0 and 0xFD (62 个 code unit); all further bytes in a multibyte sequence
  are in the range 0x80 to 0xBF (64 个 code unit).

  注意到在一个 encoding 中,
  
  * 第一个 byte (leading byte) 是 ``11xxxxxx``, 后续的所有 bytes (continuation
    byte) 都是 ``10xxxxxx``. 这样根据 bit pattern 就可以判断出字符起止. 而无需
    记录一个编码有几个 byte.

- 第一个 byte 每增加一位 leading 1, 相应的 trailing bytes 就增加一个. 也就是说,
  the number of leading 1 bit in the first byte, 等于整个编码的 byte 数目.

  由此也可以得到:

  * 一个 bytes, 可编码: ``2**7`` (128) 个.

  * 两个 bytes, 可编码: ``2**5 * 2**6`` (2048) 个.

  * 三个 bytes, 可编码: ``2**4 * (2**6)**2`` (65536) 个.

  * 四个 bytes, 可编码: ``2**3 * (2**6)**3`` (2097152) 个.

- The bytes 0xFE and 0xFF are never used. 这是为了避免与 UTF-16/32 使用的
  BOM (U+FEFF) 冲突. 将 UTF-16/32 text 误认为是 UTF-8 text.

- 长度与表示范围:
  
  * 要表示 BMP 范围字符, 需要 3 bytes.

  * 要表示目前的 unicode 标准范围 (也对应于 UTF-16 支持的范围) U+0000 -
    U+10FFFF, 需要 4 bytes.

  * 要表示 unicode 全部 2**31 个字符, 需要 6 bytes.

- Unicode code point 至 UTF-8 编码.

  * 遵守上述 ``11xxxxxx`` (62 code unit) 与 ``10xxxxxx`` (64 code unit) 规则.
    从低位至高位依次填充, 需要几个 code unit 就写几个.

- UTF-8 不需要在文件头部加 BOM (因不存在 byte order 问题). UTF-8 standard
  recommends that BOM be forbidden in protocols using UTF-8.
  
  实际上在 Unix 系统中, 更是禁止这样去做. 否则大量基本命令需要考虑处理 BOM; 并
  且对于 script file, 内核寻找 shebang line 时也需要考虑 BOM.

features and advantages
^^^^^^^^^^^^^^^^^^^^^^^
- backward-compatible with ASCII (Thus suitable for Unix environment. See
  below).

  This was the main driving force behind the design of UTF-8.

  * In UTF-8, single bytes with values in the range of 0 to 127 map directly to
    Unicode code points in the ASCII range, as they do in ASCII encoding.

  * 7-bit bytes (bytes where the most significant bit is 0) never appear in a
    multi-byte sequence, and no valid multi-byte sequence decodes to an ASCII
    code-point.

  * many text processors, parsers, protocols, file formats, text display
    programs etc., which use ASCII characters for formatting and control
    purposes will continue to work as intended by treating the UTF-8 byte
    stream as a sequence of single-byte characters, without decoding the
    multi-byte sequences.

- avoiding the complications of endianness and byte-order marks in UTF-16 and
  UTF-32.

- Self-synchronization. The leading bytes and the continuation bytes do not
  share values.  这带来的 implications:

  * a search will not accidentally find the sequence for one character starting
    in the middle of another character.

  * a shorter sequence will never appear inside a longer one.

  * the start of a character can be found from a random position by backing up
    at most 3 bytes to find the leading byte.

  * An incorrect character will not be decoded if a stream starts mid-sequence.

- Sorting order. a list of UTF-8 strings can be sorted in code point order by
  sorting the corresponding byte sequences.

UTF-8 and Unix environment
^^^^^^^^^^^^^^^^^^^^^^^^^^
- UTF-16 或 UTF-32 encoding 虽然是最自然的 unicode encoding, 但在 Unix 环境下使
  用可能带来很多问题. 因为这样编码的文件会包含很多 null char ``\x00``. 而 null
  char 在多个场景下都具有特殊含义. 例如很多 C 函数预期 char array ends by null
  char; 一些命令行工具预期参数以 null char 分隔; kernel 暴露出 environ 以 null
  char 分隔.  因此, UTF-16, UTF-32 等编码的 unicode 字符串不适合用于 filename,
  环境变量的值, etc.

- 而 UTF-8 没有这个问题, 这主要是因为它的 code unit 是 1 byte, 而不像 UTF-16,
  UTF-32 那样是多个 bytes. 这样在将每个 unicode 字符编码时, 编码后的结果不是固
  定长度的, 而是根据所需字节数来调整结果长度, 避免了 prefix null char 的问题.

- With the UTF-8 encoding, Unicode can be used in a convenient and backwards
  compatible way in environments that were designed entirely around ASCII
  (because code points are encoded with variable width), like traditional Unix.
  UTF-8 is the way in which Unicode is used under Unix, Linux, and similar
  systems.

UTF-16
------
- UTF-16 中, 每个 code unit 由 2 bytes 组成.

- UTF-16 can represent U+0000 - U+10FFFF. 这是目前 unicode 的实际定义范围,
  可通过 21-bit 来表示.

- UTF-16 包含 BE & LE 两种, UTF-16BE, UTF-16LE.

- If BE variant is in use, an ASCII or Latin-1 file can be transformed into a
  UTF-16 file by simply inserting a 0x00 byte in front of every ASCII byte.

- UTF-16 is an extension of UCS-2, to handle characters beyond BMP. It's
  backwards compatible with UCS-2.

- UTF-16 包含 BE & LE 两种, 因为它的 code unit 是 2 bytes.

- 在编码时, 未指定 endianness 时, 生成的 encoded binary text 以 BOM 为第一个
  字符. 若明确指定了 BE or LE variant, 则生成的结果不添加 BOM.

- It's a variable-width encoding. Any code point with a scalar value less than
  U+10000 (BMP) are encoded with a single code unit. Code points with a value
  U+10000 or higher (above BMP) require two code units each. These pairs of
  code units have a unique term in UTF-16: "Unicode surrogate pairs".

- Usage:
 
  * UTF-16 is often used in any originally UCS-2 based systems, e.g., windows,
    Java, etc.

UTF-32
------
- UTF-32 中, 每个 code unit 由 4 bytes 组成.

- UTF-32 包含 BE & LE 两种, UTF-32BE, UTF-32LE.

- If BE variant is in use, an ASCII or Latin-1 file can be transformed into a
  UCS-4 file by simply inserting 3 0x00 bytes in front of every ASCII byte.

- UTF-32 包含 BE & LE 两种, 因为它的 code unit 是 4 bytes.

- 在编码时, 未指定 endianness 时, 生成的 encoded binary text 以 BOM 为第一个
  字符. 若明确指定了 BE or LE variant, 则生成的结果不添加 BOM.

- encoding scheme.

  * 基本上就是把 code point 简单地塞到 4 个 bytes 的空间中.

- Usage:

  * UTF-32 is widely used as an internal representation of text in programs.

    注意准确地讲, 程序在内存中不是直接保存 unicode code point 的, 因为 code point
    是一个抽象的表 (coded character set), 无论是在内存中还是在硬盘中, 都是一种
    存储. 都是需要编码成一个一个 byte 来放置的. 只是由于内存可以同时读写多个 bytes,
    所以用 UTF-32 来保存 unicode 文字是最直接最方便的.

    例子. python unicode string is stored in UTF-32. Under Unix, C type
    ``wchar_t`` is stored in UTF-32.
 
  * UTF-32 has almost no use outside programs' internal data.

UCS-2
-----
- UCS-2 can represent only chars from BMP. U+0000 - U+FFFF.

- Each character is encoded into 2bytes.

- UCS-2, UCS-4 (UTF-32) 中, 每个字符编码的长度都是固定的. 编码同等信息, UCS-4 
  需要两倍于 UCS-2 的存储空间.

UCS-4
-----

- Essentially the same as UTF-32.

BOM
---
- Byte Order Mark (BOM). 实际上就是 U+FEFF (ZERO WIDTH NO-BREAK SPACE).
  It has the important property of unambiguity on byte reorder.

- 只有 U+FEFF 在文件起始时, 才是 BOM. 否则就是普通的 U+FEFF 字符.

- 将 BOM 字符置于文件的起始位置, 这是为了能够快速判断编码所使用的 byte order.
  实际上也可能直接区分出 UTF-16 和 UTF-32 (根据是否有 2 null bytes prefix).
  它判断 byte order 的原理是 Its byte-swapped equivalent U+FFFE is not a valid
  Unicode character, therefore it helps to unambiguously distinguish the
  Bigendian and Littleendian variants of UTF-16 and UTF-32.
