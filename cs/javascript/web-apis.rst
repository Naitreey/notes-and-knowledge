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

Event chaining
^^^^^^^^^^^^^^
- Certain events cause additional events to be dispatched.

  * E.g., mousedown event on input field leads to dispatch of focus event,
    which gets input field focused.

- Canceling the former event causes the latter event not dispatched.

Cancelable events and default actions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- A cancelable event is an event which has a cancelable default action.
  注意不是说 event itself can be canceled, 而是说它关联的默认行为 can be
  canceled.

  an event object is cancelable if ``Event.cancelable`` is true.

- An event's default action is a supplementary behavior that browser performs
  in combination with the dispatch of the event object.
  
  Each event type defines its default action (in W3C specification), if it has
  one.

  Default action is taken after event propagation is completed and handlers at
  various level of relevant DOM tree are executed.

- 注意 default actions 只有 builtin event 才会具有, 并且不可修改, 是由浏览器实
  现并自动执行的.

- Preventing an event's default action
 
  * call ``Event.preventDefault()`` method in event handler.

  * Return false from handlers assigned by ``on<event>`` attributes.


event handlers
^^^^^^^^^^^^^^
- An event handler is a defined reaction to an event. (What's the point of event
  without reactions?)

- Event handler and event flow.
  
  * When an event propagates through an element, the related event handlers are
    run in order. In event handler body, ``this`` is bound to the current
    element, which is the element the handler bound to.

  * 一般情况下 event handlers are bound to target and bubble phase, 除非使用
    ``EventTarget.addEventHandler()`` 的第三个参数指定 capture phase. 这很少使
    用.

  * handlers on both capture and bubble phases trigger at target phase.

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

event classes
-------------

Event
^^^^^
- Event is the base class of all native and custom event classes.

constructor
""""""""""""
::

  new Event(type[, options])

- ``type``. the name of the event.

- ``options``. an object with following fields:

  * ``bubbles``. a Boolean for whether the event bubbles. default false.

  * ``cancelable``. a Boolean for whether the event can be canceled. default
    false.

  * ``composed``. a Boolean for whether the event will propagate across the
    shadow DOM boundary into the standard DOM. default false.

- Event subclasses could define more fields in ``options``.

attributes
""""""""""
- ``defaultPrevented``. whether or not ``preventDefault()`` has been called.
  这与 event delegation 配合时很有用.

- ``isTrusted``. whether or not the event was initiated by the browser or by a
  script.

methods
""""""""
- ``stopPropagation()``. stop event propagation along the DOM tree. Event
  Bubbling is convenient. Don’t stop it without a real need, because we can’t
  really be sure we won’t need it above.

- ``stopImmediatePropagation()``. stop calling any other event handlers on the
  same element, and stop event propagation as well.

- ``preventDefault()``. Tells UA the predefined default action should not be
  executed and set ``defaultPrevented`` to true. It doesn't stop event
  propagation or invoking other handlers on the element.

  对于 custom events, 没有浏览器的默认行为, 但是仍然可以有 JS 代码定义的 "默认"
  行为. 此时 ``preventDefault()`` 的意义在于告诉 ``dispatchEvent()`` 的 js 脚本
  某个 handler 要求不执行这个行为.

CustomEvent
^^^^^^^^^^^
- custom events 应该使用这个 Event subclass 作为基类.

- Custom events with our own names are often generated for architectural
  purposes, to signal what happens inside a custom UI component.

constructor
""""""""""""

- additional option fields:

  * ``detail``. arbitrary information.

interfaces
----------

EventTarget
^^^^^^^^^^^

methods
"""""""

- ``addEventListener(type, listener[, options_or_usecapture])``.

  * ``listener``. an object implementing the ``EventListener`` interface, or a
    function.

- ``dispatchEvent(event)``. dispatch ``event`` at the target element. The
  ``EventTarget`` element became the ``Event.target`` of the ``event``.
  *Synchronously* going through event propagation process and invoking all
  handlers along the way.

  Return false if event is cancelable and its ``Event.preventDefault()`` has
  been called by handlers, otherwise true.

  Native DOM events 由 DOM 触发, 触发后进入 event loop 的 event queue, handlers
  are run asynchronously. 也就是说 DOM 触发 event 后会继续执行下面的逻辑, 不会
  blocking 等待所有 handlers 完成执行 (假如是单线程 event loop 这样还会导致
  deadlock). 但由 JS 代码 ``dispatchEvent()`` 触发的 event, 其执行是同步的. 它
  内部会直接走完整个处理流程再返回.

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
- keydown. a key is pressed down.

  * If the key is associated with a character, the default action is to
    dispatch a beforeinput event followed by an input event.

- keyup.

mouse events
^^^^^^^^^^^^
- click.

- contextmenu. when right click or the context menu key is pressed.

  default action: showing browser's context menu.

- mouseenter/mouseleave. triggered when a pointing device entering/leaving the
  element's boundary. 这包含该元素包裹的全部区域, 包含它的所有子元素. 只有在进
  入/离开外边界时才会触发. These events does not bubble.

- mouseover/mouseout. triggered when pointing device entering/leaving the
  element's boundary.  并且 mouseover/mouseout 都会在 entering AND leaving
  direct child element 时触发. These events does bubble. 使用 event delegation
  pattern 时, 应该使用这两个事件.

- mousedown/mouseup. when a mouse button is pressed/released.
  mousedown starts selection.

- mousemove.

wheel events
^^^^^^^^^^^^
- wheel. roll the wheel.

  * default action. scroll or zoom the document.

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
