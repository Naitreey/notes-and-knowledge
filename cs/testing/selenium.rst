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

Locating elements
=================
- 5 ways to locate an element: id, name, link text, CSS selector, XPath.

link text
---------

xpath
-----
- If there’s more than one element that matches the query, then only the first
  will be returned.

design pattern
--------------
- Which one to choose when selecting a element:
  
  * focusing first on id and link text, then CSS, and leveraging XPath only
    when you need it (e.g. walking up the DOM).

  * Choose CSS selector and XPath when you need to ensure element hierarchy.

Waits
=====

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

