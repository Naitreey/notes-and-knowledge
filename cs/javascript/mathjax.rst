general
=======
- a js math display engine for LaTeX, MathML, and AsciiMath notations.

- goal: consolidating the recent advances in web technologies into a single,
  definitive, math-on-the-web platform supporting the major browsers and
  operating systems.

- Author simply includes MathJax and some mathematics in a web page, and
  MathJax does the rest. No setup is needed on user-side.

- 使用 web fonts 矢量字体, 保证输出质量.

- mathematics is text-based rather than image-based, and so it is available for
  search engines, meaning that your equations can be searchable, just like the
  text of your pages.

- support (La)TeX, MathML, AsciiMath.

- 使用 mathjax, 连 html + latex 也成了写数学的一种方式.

(La)TeX input
=============

- 在 body element 中, tex markups 直接作为 text content 的一部分直接输入即可.
  使用标准的 tex math delimiters 加入 latex math markup 即可. 到时候 mathjax
  会自动转换.

- 默认的 displayed math delimiters 是 ``$$...$$`` & ``\[...\]``, inline
  math delimiters 是 ``\(...\)``.
