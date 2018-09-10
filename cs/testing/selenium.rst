- random notes:

  * use innerHTML/outerHTML virtual attribute to test text in source.

  * 不要检测过细致的内容. 只进行功能点存在或生效方面的检测.

overview
========
- Browser webdriver support: Firefox, Chrome, IE and Remote.

- Selenium provides webdriver client library for multiple languages.  They all
  work independently.

webdriver API
=============

python
------
- webdriver client is implemented in ``selenium.webdriver`` package.

WebDriver
^^^^^^^^^

navigation
""""""""""
- ``get(url)``. block until the page has fully loaded (``onload`` event fired).

- ``forward()``

- ``back()``

window
""""""
- ``switch_to_window(window)``

frame
"""""
- ``switch_to_frame(frame)``

- ``switch_to_default_content()``

popup dialogues
"""""""""""""""
- ``switch_to_alert()``

cookies
"""""""
- ``add_cookie(cookie)``

- ``get_cookies()``

WebElement
^^^^^^^^^^

- ``clear()``.

- ``submit()``

- ``send_keys()``

  * input file path to upload file, better use absolute path.

Locating elements
=================

python
------
- The following APIs are available on ``WebDriver`` and ``WebElement``.

id
^^

- ``find_element_by_id()``

- ``find_elements_by_id()``

name
^^^^
- ``find_element_by_name()``

- ``find_elements_by_name()``

tag name
^^^^^^^^
- ``find_element_by_tag_name()``

- ``find_elements_by_tag_name()``

class name
^^^^^^^^^^
- ``find_element_by_class_name()``

- ``find_elements_by_class_name()``

link text
^^^^^^^^^
- ``find_element_by_link_text()``

- ``find_elements_by_link_text()``

- ``find_element_by_partial_link_text()``

- ``find_elements_by_partial_link_text()``

xpath
^^^^^
- ``find_element_by_xpath()``

- ``find_elements_by_xpath()``

selector
^^^^^^^^
- ``find_element_by_css_selector()``

- ``find_elements_by_css_selector()``

generic methods
^^^^^^^^^^^^^^^
- ``find_element()``

- ``find_elements()``

- 这些方法实现了上述具体 APIs, 通过 ``selenium.webdriver.common.by.By`` class.

design pattern
--------------
- Which one to choose when selecting a element:
  
  * focusing first on simple locators, then CSS, and leveraging XPath only when
    you need it (e.g. walking up the DOM).

  * Choose CSS selector and XPath when you need to ensure element hierarchy.

Waits
=====

explicit waits
--------------
- An explicit wait is a code you define to wait for a certain condition to
  occur before proceeding further in the code. examples of explicit waits:

  * ``time.sleep()``
    
  * selenium's expected conditions.

  * custom wait polling helpers.

- 在 explicit wait 过程中, selenium polls the DOM on a fixed frequency, 直到
  condition is fullfilled or timeout is reached.

expected conditions
^^^^^^^^^^^^^^^^^^^

python
""""""
- definition: A expected condition is a callable that:

  * accepts a ``WebDriver`` instance.

  * returns False when the condition is not satisfied.

- predefined expected conditions: ``selenium.webdriver.support.exepcted_conditions``

title
~~~~~
- ``title_is``

- ``title_contains``

presence
~~~~~~~~
- ``presence_of_element_located``

- ``presence_of_all_elements_located``

visibility
~~~~~~~~~~
- ``visibility_of_element_located``

- ``invisibility_of_element_located``

- ``visibility_of``

text
~~~~
- ``text_to_be_present_in_element``

- ``text_to_be_present_in_element_value``

frame
~~~~~
- ``frame_to_be_available_and_switch_to_it``

click
~~~~~
- ``element_to_be_clickable``

stale
~~~~~
- ``staleness_of``

selection
~~~~~~~~~
- ``element_to_be_selected``

- ``element_located_to_be_selected``

- ``element_selection_state_to_be``

- ``element_located_selection_state_to_be``

alert
~~~~~
- ``alert_is_present``

implicit waits
--------------
- Apply an overall polling mechanism when trying to find any element (or
  elements) not immediately available.

- 避免使用 implicit wait, 因为指定何时需要等待、何时不需要等待这属于程序
  行为定义的一部分. 是需要检测的.

- ``WebDriver.implicitly_wait(timeout)``

design patterns
---------------
- Explicit waits 用于将浏览器的异步操作转换为同步. 即 selenium 控制端 poll 浏览
  器的状态.

utilities
=========

keys
----
- python: ``selenium.webdriver.common.keys``

UI helpers
----------
- python: ``selenium.webdriver.support.ui``

Select
^^^^^^

actions
-------
- python: ``selenium.webdriver.common.action_chains``

ActionChains
^^^^^^^^^^^^

exceptions
==========
python
------
- module: ``selenium.common.exceptions``



language bindings
=================

python
------
- selenium

recipes
=======

- Polling for element when page refreshes. web driver 需要等待页面刷新完成
  才能去执行下面的检测代码. 此时, 就需要频繁地 polling 以减少等待时间.
  可以使用以下代码:

    .. code:: python

    import time
    import unittest
    import numpy as np
    from selenium import webdriver
    from selenium.common.exceptions import WebDriverException

    class BaseTestCase(unittest.TestCase):

        max_polling = 10
        polling_interval = 0.1

        def setUp(self):
            self.driver = webdriver.Chrome()

        def wait_for_fn(self, fn, args=None, kwargs=None):
            for _ in np.arange(0, self.max_polling, self.polling_interval):
                try:
                    return fn(*(args or []), **(kwargs or {}))
                except (AssertionError, WebDriverException) as e:
                    exc = e
                    time.sleep(self.polling_interval)
            else:
                raise exc

        def wait_for_elem(self, selector):
            return self.wait_for_fn(
                lambda: self.driver.find_element_by_css_selector(selector)
            )

