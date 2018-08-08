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

prompt()
--------

alert()
-------

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
