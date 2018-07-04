components
==========

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

