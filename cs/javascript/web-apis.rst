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

  * mimlength/maxlength is suitable for text-like inputs and textarea.

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

- ``setCustomValidity(message)``. Sets a custom error message to the element
  when it's considered invalid. The specified error is displayed. If the
  argument is the empty string, the custom error is cleared.

form element APIs
"""""""""""""""""
properties.

- ``noValidate``. boolean as to html attribute.

methods.

- ``checkValidity()``. true if all form controls are valid, false otherwise.
  Fires an event named ``invalid`` at any control that does not satisfy its
  constraints; such controls are considered invalid if the event is not
  canceled.


validation process
^^^^^^^^^^^^^^^^^^
- Constraint validation can be done on a single form element individually or at
  the entire form level.

- If an element's input data satisfies validation constraints, the element
  matches ``:valid`` css pseudo-class, otherwise it matches ``:invalid``
  pseudo-class.

- When user submits the form, the browser only allows form submission if all
  form control elements are valid.  Otherwise the form submission is blocked
  and built-in form validation message feedback is displayed on related fields.

- automatic generated feedback 的缺点:
  
  * 对每次用户提交, Built-in validation feedback 只显示第一个 invalid
    field 相应的错误提示.

  * no standard way to change their look and feel with CSS.

  * 信息只能通过 js API 去自定义, 不能写在 html 中.

  * 信息输出的语言可能与页面语言不一致.

Console
=======

log()
-----
