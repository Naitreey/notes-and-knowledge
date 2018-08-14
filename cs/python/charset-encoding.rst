chardet
=======

overview
--------
- character encoding detection library written in python.

- chardet is a port of Mozilla Charset Detectors used by mozilla in firefox for
  character encoding detection.

- 编码检测的大致原理, 就是从不同编码的特征、不同文字和语言的特征等方面入手, 去
  推断二进制信息的编码. 这就像是给你一段不知什么语言写的文字, 然后判断这是什么
  语言 (并解析它的内容). 这也能看出 Character encoding detection 不可能做到完全
  准确. 

  编码检测需要训练模型, By studying lots of “typical” text, a computer
  algorithm can simulate this kind of fluency and make an educated guess about
  a text’s language. 这有点像神经网络.

  Encoding detection is really language detection, combined with knowledge of
  which languages tend to use which character encodings.

- character encoding detection should be used as a last resort. Whenever more
  explicit indication/standard source of encoding is available, use that.

supported encodings
-------------------
- See https://chardet.readthedocs.io/en/latest/supported-encodings.html

- some of commons:
  ascii, windows-1252/iso-8859-1, big5, gb2312/gb18030, utf-8, utf-16, utf-32.

model-level functions
---------------------

- ``detect(bytes)``. 这是最直接的用法. input must be a byte string. return a
  dict::

    {"encoding": "...", "confidence": 0.x, "language": "..."}

  confidence is between 0-1.

universaldetector
-----------------

UniversalDetector
^^^^^^^^^^^^^^^^^

- 这个 class 适用于检测大体积的文本, 这时就不适合一次读入内存了. 所以这里是流处理.

- 基本用法:
  
  * Create a UniversalDetector object, then call its ``feed()`` method repeatedly
    with each block of text.

  * If the detector reaches a minimum threshold of confidence, it will set ``done``
    attribute to True.

  * When detection is finished or source is exhausted, call ``close()`` method,
    which will do some final calculations in case the detector didn’t hit its
    minimum confidence threshold earlier.

  * ``result`` attribute will be a dictionary containing the same info as
    ``chardet.detect()`` output.

attributes
""""""""""
- ``done``

- ``result``

methods
""""""""
- ``feed(bytes)``

- ``close()``

- ``reset()``. Reset detector. 重置之后同一个 detector 可以用于检测另一个文件.

CLI
---
::

  chardetect [input]...
