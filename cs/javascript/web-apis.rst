overview
========
- What is WebAPI?
  
  WebAPI is the programming interface provided by browser, to interact with browser.
  
  与系统层编程去类比, 浏览器提供的 Web API 就相当于是 OS kernel 提供的操作系统 API.
  浏览器在 web 中的地位相当于操作系统. JS 之于 browser 就相当于 C/Python 之于 kernel.
  JS 存在语言部分与 WebAPI 部分, C 存在语言部分与操作系统 API 部分. 后一部分都是由
  应用平台决定的.

Window
======
- ``Window`` is main object root, the global object in a browser.
  A ``Window`` is also the root of the DOM tree.

- Window defines the properties of browser window/tab.

prompt()
--------

alert()
-------

document
========

- ``Document`` is a direct child of ``Window``. Available as ``Window.document``,
  therefore also bare ``document``.

- A document is the main object of the visible DOM (in combination with
  iframes, etc.). It is loaded inside a ``Window``.

attributes
----------

- ``documentElement``. The root element of the ``Document``. For a html doc, it's
  ``<html>`` DOM element.

- ``head``

- ``body``

WindowOrWorkerGlobalScope
=========================

setInterval()
-------------

setTimeout()
------------

form
====

form data structure
-------------------
- ``FormData`` 是 form 数据的封装. 本质上, it represents a set of key/value
  pairs such as form fields and their values. 但显然不限于 form data, 而是
  任何格式相符的数据.

- It uses the same format a form would use if the encoding type were set to
  ``multipart/form-data``.

- Usage:

  * conveniently build form data and send via ajax requests.

form validation
---------------

- Form validation is termed constraint validation.

- constraint validation is based on two mechanisms:

  * semantic types of form controls and constraint attributes. (intrinsic
    constraints)
    
    This form of validation does not require js code and is performed by
    browser. It's technically faster and simpler.

  * constraint validation javascript API.
    
    Completely customizable, suitable for custom validation requirements.

intrinsic constraints
^^^^^^^^^^^^^^^^^^^^^
See `forms` section in  `../html-css/language.rst` for details on input types
and validation attributes.

- semantic input types: date, time, datetime-local, month, week, tel, email,
  url, number, range, search, password.
  
  其中自带格式要求的有: date, time, datetime-local, month, week, email, url,
  number, range. 这些自带格式要求的 input 本质上就是存在一个默认的 ``pattern``
  属性值.

- constraint attributes: required, pattern, min, max, step, minlength,
  maxlength.

  * required is suitable for all form controls.

  * pattern is suitable for text-like inputs.

  * minlength/maxlength is suitable for text-like inputs and textarea.

  * min, max, step is suitable for number-like and date-like inputs.

constraint validation API
^^^^^^^^^^^^^^^^^^^^^^^^^

form control APIs
""""""""""""""""""
properties. 所有属性值都是根据 DOM element 状态实时刷新的.

- ``willValidate``. true if the element will be validated on form submission.
  Only be false if the element is disabled.

- ``validationMessage``. 当前输入所对应的 validation feedback message. If
  input is valid, or when ``willValidate`` is false, it's empty string.

- ``validity``. A ``ValidityState`` object encapsulating the detailed
  validation info of current input.

methods.

- ``checkValidity()``. true if valid, false otherwise. An ``invalid`` event is
  also fired if the input is invalid.

- ``setCustomValidity(message)``. Sets a custom error message to the element's
  ``validationMessage``. This also makes the input invalid. The specified
  message is displayed when form's ``reportValidity()`` is called. If the
  argument is the empty string, the custom error is cleared.

form element APIs
"""""""""""""""""
properties.

- ``noValidate``. boolean as to html attribute.

  ``noValidate`` attribute 决定在 form submission 时, 是否 ``reportValidity()``
  以及如果 validation failed 的话, 是否 suppress form submission. 它不影响其他
  任何方面, 例如不影响每个 field 的实时 validation check 以及相应的
  pseudo-class 状态应用. 即使 ``noValidate``, 仍然可以在 js 中 call this
  method and triggers feedback.

methods.

- ``checkValidity()``. true if all form controls are valid, false otherwise.
  Fires an event named ``invalid`` at any control that does not satisfy its
  constraints; such controls are considered invalid if the event is not
  canceled.

- ``reportValidity()``. similar to ``checkValidity()``, 同时会立即显示 form
  control 的 validation feedback.

validation process
^^^^^^^^^^^^^^^^^^
- 对每个 form control, 在页面加载完成时, 以及在 ``input`` event 发生时, 会自动
  检查输入合法性. If an element's input data satisfies validation constraints,
  the element matches ``:valid`` css pseudo-class, otherwise it matches
  ``:invalid`` pseudo-class.

  这可通过 ``input`` event handler 以及 constraint validation API 来自定义.

- When user submits the form, 浏览器自动检查每个 form control 的合法性. It only
  allows form submission if all form control elements are valid. Otherwise the
  form submission is blocked and built-in form validation message feedback is
  displayed on related fields.

  这可通过 ``submit`` event handler 以及 constraint validation API 来自定义.

client-server communication
===========================

AJAX
----
- ajax 最初设计时以 xml 为传输使用的数据格式, 后来一般化了, 什么格式都可以.

Console
=======

log()
-----

Event Model
===========
- Event-driven 是 JS 的核心特征之一.

- 在不同的 host environment 中, 以及和不同的框架交互时, 会有不同的 event 类型
  和处理机制. 例如在浏览器中, 就是 DOM 相关的一套机制.

DOM Event Architecture
----------------------

Event dispatch
^^^^^^^^^^^^^^
- Event dispatch is the process of creating an event with appropriate
  attributes and methods and propagating it through the DOM tree.

- Event can be dispatched by UA or by ``EventTarget.dispatchEvent()`` method.
  After dispatch, the event object is propagated throught the DOM tree as
  determined by the DOM event flow.

DOM event flow
^^^^^^^^^^^^^^
- A dispatched event is propagated through a propagation path, which is an
  ordered list of current event targets through which an event object will pass
  sequentially on the way to and back from the event target.

  The last item in the list is the event target, and the preceding items in the
  list are referred to as the target’s ancestors, with the immediately preceding
  item as the target’s parent.

- There are 3 phases during an event propagation.

  * capture phase. The event object propagates through the target’s ancestors
    from the ``Window`` to the target’s parent.

  * target phase. The event object arrives at the event object’s event target.

  * bubble phase. The event object propagates through the target’s ancestors in
    reverse order, starting with the target’s parent and ending with the
    ``Window``.

  Some of the phases can be skipped by setting ``Event`` object's attributes or by
  calling ``Event.stopPropagation()`` method.
  
- As the event propagates, each current event target in the propagation path is
  in turn set as the ``currentTarget``. ``Event.target`` is the initiating
  event target.
  
- Event handler and event flow.
  
  * When an event propagates through an element, the related event handlers are
    run in order. In event handler body, ``this`` is bound to the current
    element, which is the element the handler bound to.

  * 一般情况下 event handlers are bound to target and bubble phase, 除非使用
    ``EventTarget.addEventHandler()`` 的第三个参数指定 capture phase. 这很少使
    用.

  * handlers on both capture and bubble phases trigger at target phase.

Cancelable events and their default actions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- A cancelable event is an event which has a cancelable default action.
  注意不是说 event itself can be canceled, 而是说它关联的默认行为 can be
  canceled.

  an event object is cancelable if ``Event.cancelable`` is true.

- An event's default action is a supplementary behavior that UA performs
  in combination with the dispatch of the event object.
  
  Each event type defines its default action, if it has one.

- To cancel an event's default action, call ``Event.preventDefault()`` method.

event handlers
^^^^^^^^^^^^^^
- An event handler is a defined reaction to an event. What's the point of event
  without reactions?

- Three ways to specify handlers to events:

  * Set element's html attributes ``on<event>``, whose value is event handler
    code wrapped in double-quotes. Event handler code is wrapped by an
    anonymous function::

      function (event) {
        // handler code
      }

  * Set element's DOM attributes ``on<event>``, whose value is an event handler
    callable.

    To remove a handler, set attribute to ``null``.

  * Use ``EventTarget.addEventListener()`` to register possibly multiple
    handlers for the same event.

    Use ``EventTarget.removeEventListener()`` to remove handlers.

  Notes:
  
  * Don't use ``Element.setAttribute()`` for handlers, because attributes
    are always strings. This would coerce handler to string.

  * All events can be set with ``addEventListener()``, but not all can be set
    with ``on<event>``.

  * ``on<event>`` attribute 设置的 handler 与 ``addEventListener()`` 的不会
    冲突, 会一起生效.

- The value of ``this`` inside a handler function is the element whose handler
  is called (除非对于 arrow function 则是 lexical ``this``).

Event
-----

methods
^^^^^^^
- ``stopPropagation()``. stop event propagation along the DOM tree. Event
  Bubbling is convenient. Don’t stop it without a real need, because we can’t
  really be sure we won’t need it above.

- ``stopImmediatePropagation()``. stop calling any other event handlers on the
  same element, and stop event propagation as well.

interfaces
----------

EventTarget
^^^^^^^^^^^

methods
"""""""

- ``addEventListener(type, listener[, options_or_usecapture])``.

  * ``listener``. an object implementing the ``EventListener`` interface, or a
    function.

event types
-----------

document events
^^^^^^^^^^^^^^^
- DOMContentLoaded. when the initial HTML document has been completely loaded
  and parsed, without waiting for stylesheets, images, and subframes to finish
  loading.

  This is different from ``load`` event fired on ``document``, which detects a
  fully-loaded page.

CSS events
^^^^^^^^^^
- transitionend.

mouse events
^^^^^^^^^^^^
- click.

- contextmenu. right click.

- mouseenter/mouseleave. triggered when a pointing device entering/leaving the
  element's boundary. 这包含该元素包裹的全部区域, 包含它的所有子元素. 只有在进
  入/离开外边界时才会触发. These events does not bubble.

- mouseover/mouseout. triggered when pointing device entering/leaving the
  element's boundary.  并且 mouseover/mouseout 都会在 entering AND leaving direct
  child element 时触发. These events does bubble.

- mousedown/mouseup. when a mouse button is pressed/released.

- mousemove.

form events
^^^^^^^^^^^
- submit.

- change.

- reset.

focus events
^^^^^^^^^^^^
- focus.

- blur.

keyboard events
^^^^^^^^^^^^^^^
- keydown.

- keyup.

design patterns
---------------
- event delegation. If we have a lot of elements with event handled in a
  similar way, then instead of assigning a handler to each of them – we put a
  single handler on their common ancestor.

  benefits:

  * Simplifies initialization and saves memory (no need to add many handlers).

  * less code and better consistency.

  limitations:

  * the event must be bubbling. low-level handlers should not
    ``Event.stopPropagation()``.

References
==========

.. [W3DOMUIEvents] `UI Events W3C Working Draft, 04 August 2016 <https://www.w3.org/TR/DOM-Level-3-Events/#event-flow-default-cancel>`_
