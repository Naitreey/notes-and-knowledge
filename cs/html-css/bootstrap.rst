overview
========

- A component library (not a framework)

- features

  * responsive
   
  * mobile-first

- JS dependencies (in loading order)

  * jquery

  * popper.js

- browser compatibility:
  
  * latest, stable releases of all major browsers.

package content
===============

- ``*.map`` is map file used for debugging.

css
---

- ``bootstrap[.min].css`` include all modules: layout, content, components, utilities.
  Without ``.min``, is just source files compiled together. With ``.min``, also minified.

- ``bootstrap-grid[.min].css`` includes: grid layout system and flex utilities.

- ``bootstrap-reboot[.min].css`` includes: reboot content module.

js
--

- ``bootstrap[.min].js`` include bootstrap js library.

- ``bootstrap.bundle[.min].js`` include also popper.js library.

- In source distro, there is individual js files for each components under ``js/dist/``.

setup
=====

- viewport tag::

    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

- bootstrap css tag.

- jquery, popper.js, bootstrap script tags.

global styles
=============

- change all elements' box-sizing to ``border-box``.

data api
========

- Nearly all Bootstrap plugins can be enabled and configured through HTML alone
  with data attributes.

- To disable the data attribute API, unbind all events on the document
  namespaced with ``data-api``. to target a specific plugin, just include the
  plugin’s name as a namespace along with the ``data-api`` namespace.

evnets
======

- Custom events for most plugins’ unique actions.

- Custom events come in an infinitive and past participle form - where the
  infinitive (ex. show) is triggered at the start of an event, and its past
  participle form (ex. shown) is triggered on the completion of an action.

- All infinitive events provide preventDefault() functionality. This provides
  the ability to stop the execution of an action before it starts.

APIs
====

- All public APIs are single, chainable methods, and return the collection
  acted upon.

- All methods should accept an optional options object, a string which targets
  a particular method, or nothing (which initiates a plugin with default
  behavior).

- Each plugin also exposes its raw constructor on a ``Constructor`` property:
  ``$.fn.popover.Constructor``. If you’d like to get a particular plugin
  instance, retrieve it directly from an element:
  ``$('[rel="popover"]').data('popover')``.

- You can change the default settings for a plugin by modifying the plugin’s
  ``Constructor.Default`` object.

- call ``.noConflict`` on the plugin you wish to revert the value of to its
  previously assigned value.

- The version of each of Bootstrap’s jQuery plugins can be accessed via the
  ``VERSION`` property of the plugin’s constructor.

layout
======

breakpoints
-----------
breakpoints are defined in px, because viewport is computed in pixel.

- xs.
  
  * extra small.
    
  * 0 - 576px

- sm.
  
  * small.
    
  * 576px - 768px

- md.
  
  * medium.
    
  * 768px - 992px

- lg.
  
  * large.
    
  * 992px - 1200px

- xl.
  
  * extra large.

  * 1200px - inf.

media queries
-------------

sass mixins:

- ``media-breakpoint-up($width)``

- ``media-breakpoint-down($width)``

- ``media-breakpoint-only($width)``

- ``media-breakpoint-between($low, $high)``

stacking context
----------------

- sass z-index variables::

    $zindex-dropdown:          1000 !default;
    $zindex-sticky:            1020 !default;
    $zindex-fixed:             1030 !default;
    $zindex-modal-backdrop:    1040 !default;
    $zindex-modal:             1050 !default;
    $zindex-popover:           1060 !default;
    $zindex-tooltip:           1070 !default;

- To handle overlapping borders within components, we use low single digit
  z-index values of 1, 2, and 3 for default, hover, and active states.

- On hover/focus/active, we bring a particular element to the forefront with a
  higher z-index value to show their border over the sibling elements.

flexbox grid system
-------------------
- bootstrap's grid system is built with css flexbox layout.

containers
^^^^^^^^^^
- Containers has the following purposes.
  
  * provide a means to horizontally center site's content.

  * provide a responsive global width constraints.

- Container should be a global wrapper, it should never be nested.

- Container has a 15px left/right padding, so that the content doesn’t touch
  the edge of the browser.

types of containers
"""""""""""""""""""

- fixed-width container:

  * class: ``.container``
 
  * container's ``max-width`` changes at each breakpoint (by media query). 也就
    是说, 在 viewport 为某个宽度阈值与下一个阈值之间时, 限制 container 的宽度不
    能超过某个值.

- full-width container: 

  * class: ``.container-fluid``

  * spanning the entire width of the viewport. (``width: 100%`` without
    ``max-width`` constraints.)

rows
^^^^
- Rows are wrappers for columns.

  * class: ``.row``

- a row is a flexbox container.

- a row has -15px left/right margin, this pushes row's border box (由于默认没有
  border and padding, 也就意味着 content box) 与 container border box 接壤.  这
  个操作的意义是, 避免 container, row, column 三层嵌套导致 column content
  indented too much.

- never use a row outside of container, it doesn't work.

- The direct children of a row must be a set of columns.

- the margins on rows and paddings on columns can be removed by ``.no-gutters``
  class.

columns
^^^^^^^
- contents must be placed inside columns.

- Each column has 15px left/right padding (called a gutter) for controlling the
  space between columns.
  
  这个 15px 让 column 在作为 row 的第一个子元素时, 又获得了离 viewport 边界
  15px 的 padding. 并让 columns 之间有 30px 的 padding.

- 在 column 中, 还可以创建 nested grids. 这时, 需要在 column 中创建 child rows.
  在 rows 中再创建 columns.

  注意到此时外层的 column 与顶层的 container 处于相同的地位. 而 row 的 -15px
  margin 与 column 的 15px padding 抵消, 让内层 columns 不至于过度地 indent.
  这充分体现了 row 的 -15px margin 的意义.

- columns without a specified width (e.g. by column width classes) will
  automatically layout as equal width columns. This is achieved by ``flex``
  property.

- columns width classes 体现一个列的宽度占到总宽度的比例, 总宽度设置为 12.

- Column widths are set in percentages, so they’re always fluid and sized
  relative to their parent element.

column classes
""""""""""""""
- class format::

  .col[-{breakpoint}]-{width}

- breakpoint 对应于 `breakpoints`_ 定义的 5 类宽度范围.
  
- 该 class 的意义为当 viewport 宽度大于相应 breakpoint 的宽度值时, ``{width}``
  所指定的 flexbox proportional 效果才得到应用. 否则, column 占到 viewport 的全
  部宽度.

- 对于 xs, 不指定 breakpoint, 因为是从 0 开始. 此时, ``{width}`` proportional
  效果总是成立.

- ``{width}`` 最大是 12.

references
==========

.. [WhyBS3GridWorks] `The Subtle Magic Behind Why the Bootstrap 3 Grid Works <http://www.helloerik.com/the-subtle-magic-behind-why-the-bootstrap-3-grid-works>`_
