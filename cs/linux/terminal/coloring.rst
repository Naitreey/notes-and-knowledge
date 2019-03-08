- color sequence format -- ISO 6429. ISO 6429 color sequences are composed of
  sequences of numbers separated by semicolons. Multiple styles, colors and
  background colors can be combined, 也就是说不必局限于 ``fg;bg`` 格式, 可以
  任意多个组合, 例如 ``01;05;40;31``, styles, colors, background colors 没有
  固定的先后顺序.

- color definitions

  * possible styles::

      0   = default colour
      1   = bold
      4   = underlined
      5   = flashing text (disabled on some terminals)
      7   = reverse field (exchange foreground and background color)
      8   = concealed (invisible)

  * possible colors::

      31  = red
      32  = green
      33  = orange
      34  = blue
      35  = purple
      36  = cyan
      37  = grey
      90  = dark grey
      91  = light red
      92  = light green
      93  = yellow
      94  = light blue
      95  = light purple
      96  = turquoise
      97  = white

  * possible background colors::

      40  = black background
      41  = red background
      42  = green background
      43  = orange background
      44  = blue background
      45  = purple background
      46  = cyan background
      47  = grey background
      100 = dark grey background
      101 = light red background
      102 = light green background
      103 = yellow background
      104 = light blue background
      105 = light purple background
      106 = turquoise background
      107 = white background

- ISO 6429 terminal generate colored text in the following format::

    LEFTCODE typecode RIGHTCODE text ENDCODE

  where the typecode is the configured color sequence.

  The purpose of the left- and rightcodes is merely to reduce the amount of
  typing necessary (and to hide ugly escape codes away from  the  user).
