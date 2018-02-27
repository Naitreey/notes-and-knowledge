RandR
=====
- RandR: Resize and Rotate.

- randr 是 x11 protocol 的一个 extension. 负责屏幕显示相关设置.

xrandr
======
xrandr is an implementation of RandR X11 protocol extension.

common operations
-----------------

- show current state of outputs::
    xrandr [--query] [--verbose]
  with a '+' after the preferred modes and a '*' after the current mode.

- when modifying output options, multiple outputs may be modified at the same
  time by passing multiple ``--output`` options followed immediately by their
  corresponding modifying options::
    xrandr --output <o1> ... --output <o2> ...

- set as primary output::
    --primary

- turn a monitor on and set prefered mode (resolution + rate), if it's off::
    --auto

- set prefered mode only::
    --preferred

- turn a monitor off::
    --off

- set monitor resolution::
    --mode <mode>
    
- set monitor refresh rate::
    --rate <rate>

- set monitor direction::
    --rotate {normal|left|right|inverted}

- position the specified output relative to another output::
    {--left-of|--right-of|--above|--below|--same-as} another-output

- reflect output at some axis, 镜面对称::
    --relect {normal|x|y|xy}

- 缩放输出::
    --scale <X>x<Y>
