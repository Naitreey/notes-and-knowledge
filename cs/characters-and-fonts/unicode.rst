Unicode
=======
overview
--------
- The Unicode standard is a standard for consistent handling of text expressed
  in most of the world's writing systems.

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

- combining character. A combining character is not a full character by itself.
  It is an accent or other diacritical mark that is added to the previous
  character. The combining-character mechanism allows one to add accents and
  other diacritical marks to any character.

- precomposed character. The most important accented characters, like those
  used in the orthographies of common languages, have codes of their own in UCS
  to ensure backwards compatibility with older character sets. 

relation with Unicode
---------------------
- The Unicode standard and ISO/IEC 10646 are two different standards published
  by different organizations that essentially defines the same character set.
  Their code tables are always in sync.

- ISO 10646 is not much more than a simple character set table. While Unicode
  standard contains some useful additional information, including algorithms
  for rendering scripts, for sorting and string comparisons, etc.

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

scheme
^^^^^^
- ASCII subset (U+0000 to U+007F) are encoded by 1 byte, from 0x00 to 0x7F.
  This is identical to ASCII encoding.

- ASCII 之外的字符 are encoded as a sequence of several bytes, 其中的每个 byte
  has the most significant bit set. 这样的意义是两点:

  * 避免任何一个 byte 是 null char.

  * 由于 ASCII 以外字符的编码保证每个 code unit 最高位都是 1, 这样不会误将
    ASCII 字符识别为其他字符的一部分. (注意到 utf-8 没有固定的编码长度, 所以需
    要这种机制避免误识别.)

- The first byte of encoding of a non-ASCII character is always in the range of
  0xC0 and 0xFD (62 个 code unit); all further bytes in a multibyte sequence
  are in the range 0x80 to 0xBF (64 个 code unit).

  注意到在一个 encoding 中,
  
  * 第一个 byte 是 ``11xxxxxx``, 后续的所有 bytes 都是 ``10xxxxxx``. 这样根据
    bit pattern 就可以判断出字符起止. 而无需记录一个编码有几个 byte.

  * 第一个 byte 的 leading 1 bit 数目, 等于整个编码的 byte 数目.

- The bytes 0xFE and 0xFF are never used.

- 长度与表示范围:
  
  * 要表示 BMP 范围字符, 需要 3 bytes.

  * 要表示 UTF-16 范围 U+0000 - U+10FFFF, 需要 4 bytes. 这是目前的 unicode 标准
    范围.

  * 要表示 unicode 全部 2**31 个字符, 需要 6 bytes.

- unicode code point 至 UTF-8 编码的转换.

  * 遵守上述 ``11xxxxxx`` (62 code unit) 与 ``10xxxxxx`` (64 code unit) 规则.
    从低位至高位依次填充, 需要几个 code unit 就写几个.

- UTF-8 不需要在文件头部加 BOM (因不存在 byte order 问题). 并且, 在 Unix 系统中,
  更是禁止这样去做. 否则大量基本命令需要考虑处理 BOM; 并且对于 script file, 内
  核寻找 shebang line 时也需要考虑 BOM.

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

- UTF-16 is backwards compatible with UCS-2.

- UTF-16 包含 BE & LE 两种, 因为它的 code unit 是 2 bytes.

- 在编码时, 未指定 endianness 时, 生成的 encoded binary text 以 BOM 为第一个
  字符. 若明确指定了 BE or LE variant, 则生成的结果不添加 BOM.

UTF-32
------
- UTF-32 中, 每个 code unit 由 4 bytes 组成.

- UTF-32 包含 BE & LE 两种, UTF-32BE, UTF-32LE.

- If BE variant is in use, an ASCII or Latin-1 file can be transformed into a
  UCS-4 file by simply inserting 3 0x00 bytes in front of every ASCII byte.

- UTF-32 包含 BE & LE 两种, 因为它的 code unit 是 4 bytes.

- 在编码时, 未指定 endianness 时, 生成的 encoded binary text 以 BOM 为第一个
  字符. 若明确指定了 BE or LE variant, 则生成的结果不添加 BOM.

UCS-2
-----
- UCS-2 can represent only chars from BMP. U+0000 - U+FFFF.

- Each character is encoded into 2bytes.

UCS-4
-----

- Essentially the same as UTF-32.

BOM
---
- Byte Order Mark (BOM). 实际上就是 U+FEFF (ZERO WIDTH NO-BREAK SPACE).

- 将 BOM 字符置于文件的起始位置, 这是为了能够快速判断编码所使用的 byte order.
  实际上也可能直接区分出 UTF-16 和 UTF-32 (根据是否有 2 null bytes prefix).
  它判断 byte order 的原理是 Its byte-swapped equivalent U+FFFE is not a valid
  Unicode character, therefore it helps to unambiguously distinguish the
  Bigendian and Littleendian variants of UTF-16 and UTF-32.
