overview
========
- Selenium is a software-testing library for web applications.

- Selenium 主要用于 FT/AT. 它是从应用外部进行的测试.

- naming: The name Selenium comes from a joke made by Huggins in an email,
  mocking a competitor named Mercury, saying that you can cure mercury
  poisoning by taking selenium supplements. The others that received the email
  took the name and ran with it.

compontents
-----------

Selenium RC
^^^^^^^^^^^
- legacy. deprecated.

Selenium IDE
^^^^^^^^^^^^
- what is this? seems unnecessary.

Selenium WebDriver
^^^^^^^^^^^^^^^^^^
- 这是如今使用 selenium 的主要方式.

- Browser webdriver support: Firefox, Chrome, IE and Remote.

- Selenium provides webdriver client library for multiple languages.  They all
  work independently.

Selenium Grid
^^^^^^^^^^^^^
- Selenium Grid is a server that allows tests to use web browser instances
  running on remote machines.

- With Selenium Grid, one server acts as the hub. Tests contact the hub to
  obtain access to browser instances. The hub has a list of servers that
  provide access to browser instances (WebDriver nodes), and lets tests use
  these instances. Selenium Grid allows running tests in parallel on multiple
  machines, and to manage different browser versions and browser configurations
  centrally (instead of in each individual test).

webdriver API
=============

python
------
- webdriver client is implemented in ``selenium.webdriver`` package.

WebDriver
^^^^^^^^^

constructor
"""""""""""
- ``command_executor='http://127.0.0.1:4444/wd/hub'``. url of the remote server
  or a custom RemoteConnection object.

- ``desired_capabilities=None``.

- ``browser_profile=None``. only for firefox profile.

- ``proxy=None``.

- ``keep_alive=False``. use HTTP keepalive.

- ``file_detector=None``.

- ``options=None``. driver Option instance.

info
""""
- ``name``. browser name.

- ``title``. title of current page.

- ``page_source``. source of current page.

- ``desired_capabilities``.

switching
"""""""""
- ``switch_to``. object to switch focus. See `SwitchTo`_.

navigation
""""""""""
- ``current_url``.

- ``get(url)``. block until the page has fully loaded (``onload`` event fired).

- ``refresh()``.

- ``forward()``

- ``back()``.

- ``quit()``. quit browser.

- ``WebDriver.set_page_load_timeout(seconds)``. timeout for page loading.

window
""""""
- ``current_window_handle``. current window's handle.

- ``window_handles``. handles of all windows in the current session. probably
  populated in the openning order.

- ``close()``. close current window.

- ``fullscreen_window()``. make window fullscreen.

- ``maximize_window()``

- ``minimize_window()``

- ``get_window_position(windowHandle='current')``. return a dict of x, y
  position.

- ``set_window_position(x, y, windowHandle='current')``.

- ``get_window_size(windowHandle='current')``. return width and height of
  current window.

- ``set_window_size(width, height, windowHandle='current')``.

- ``get_window_rect()``. window's x, y position as well as its height and
  width.

- ``set_window_rect(x=None, y=None, width=None, height=None)``.

frame
"""""

popup dialogues
"""""""""""""""

locating
""""""""
- See `Locating elements`_.

cookies
"""""""
- ``add_cookie(cookie)``. a cookie dict with required keys: name, value;
  optional keys: path, domain, secure, expiry.

- ``get_cookies()``. a list of cookie dicts in browser session.

- ``delete_all_cookies()``. delete all cookies in browser session.

- ``delete_cookie(name)``.

scripting
""""""""""
- ``execute_script(script, *args)``. execute js synchronously in current
  window/frame.

- ``execute_async_script(script, *args)``. ditto asynchronously.

- ``set_script_timeout(seconds)``. timeout for async script execution.

screenshot
""""""""""
- ``get_screenshot_as_base64()``. return base64 string.

- ``get_screenshot_as_file(filename)``. filename should be a full path.
  return boolean for operation success.

- ``save_screenshot(filename)``. ditto.

- ``get_screenshot_as_png()``. return bytes of png data.

waits
"""""
see `implicit waits`_.

file detector
"""""""""""""
- ``file_detector``.

- ``file_detector_context(detector_class, *args, **kwargs)``. context manager
  to override current file detector temporarily.

application cache
"""""""""""""""""
- ``application_cache``. browser's ApplicationCache.

mobile
""""""
- ``mobile``. Mobile instance.

- ``orientation``. screen orientation.

utils
""""""
- ``log_types``. available log types.

- ``create_web_element(element_id)``.

- ``execute(driver_command, params=None)``. execute command remotely by
  webdriver. returns command's json response.

- ``start_session(capabilities, browser_profile=None)``. start a new session.

- ``get_log(type)``.

hooks
"""""
- ``start_client()``. hook to run before starting webdriver.

- ``stop_client()``. hook to run after stopping webdriver.


Firefox WebDriver
^^^^^^^^^^^^^^^^^

Chrome WebDriver
^^^^^^^^^^^^^^^^
constructor
"""""""""""
- ``desired_capabilities=None``.

- ``options=None``. an instance of ``ChromeOptions``.

- ``executable_path="chromedriver"``. passed to webdriver service.

- ``port=0``. default use any free port. passed to webdriver service.

- ``service_args=None``. passed to webdriver service.

- ``service_log_path=None``. passed to webdriver service.

methods
"""""""
- ``create_options()``. create a ChromeOptions instance.

- ``get_network_conditions()``.

- ``set_network_conditions(**network_conditions)``.

- ``launch_app(id)``. launch chrome browser by id.

- ``quit()``. shutdown browser and webdriver.

Chrome WebDriver Options
^^^^^^^^^^^^^^^^^^^^^^^^
- options that customize chrome browser, such as install extension, browser cli
  options, headless mode, enable experimental options, etc.

Chrome WebDriver Service
^^^^^^^^^^^^^^^^^^^^^^^^
- used by WebDriver, to encapsulate WebDriver service.

Internet Explorer WebDriver
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Android WebDriver
^^^^^^^^^^^^^^^^^

Opera WebDriver
^^^^^^^^^^^^^^^

PhantomJS WebDriver
^^^^^^^^^^^^^^^^^^^

Safari WebDriver
^^^^^^^^^^^^^^^^

WebElement
^^^^^^^^^^
- All method calls will do a freshness check to ensure that the element
  reference is still valid.

constructor
""""""""""""
- ``parent``.

- ``id_``.

- ``w3c=False``.

attributes
""""""""""
- ``id``. internal id of element. used by equality checking.

- ``parent``. the parent webdriver.

- ``tag_name``. element's tag name.

- ``text``. element's text content. 这包含所有 subelements 的 text 内容, 但不包
  含任何 markup 部分.

- ``location``. element location.

- ``location_once_scrolled_into_view``. scroll element into view and return its
  location.

- ``rect``. element's size and location.

element state
""""""""""""""
- ``is_displayed()``. visible.

- ``is_enabled()``. enabled (form control).

- ``is_selected()``. selected (form control).

locating
""""""""
find elements within this WebElement. See `Locating elements`_.

dom
"""
- ``get_attribute(name)``. first try property, then try attribute, finally
  return None. Boolean-like values are converted to True/False.

- ``get_property(name)``. get property value.

- ``value_of_css_property(name)``. css property value.

actions
""""""""
- ``click()``

input
"""""
- ``send_keys()``. typing into element.

  * input file path to upload file, better use absolute path.

- ``clear()``.

form
""""
- ``submit()``

screenshot
""""""""""
- ``screenshot(filename)``. screenshot current element to png file.

WebDriver Mobile
^^^^^^^^^^^^^^^^

Remote Connection
^^^^^^^^^^^^^^^^^

Command
^^^^^^^
- constants for WebDriver commands.

SwitchTo
^^^^^^^^
- ``selenium.webdriver.remote.switch_to``.

attributes
""""""""""
* ``active_element``. the the element that currently holds focus.

* ``alert``. alert dialogue.

methods
"""""""
* ``default_content()``. switch to default frame.

* ``frame(reference)``. switch focus to the specified frame.

* ``parent_frame()``. switch focus to parent frame.

* ``window(name)``. switch focus to window name.

error handler
^^^^^^^^^^^^^
ErrorCode
""""""""""
- Error codes defined in the WebDriver wire protocol.

ErrorHandler
""""""""""""

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
xpath 在一些复杂的定位场景下, css selector 并不能满足需求. 此时需要 xpath. 例如,
locate by element text.

WebDriver API 和 WebElement API 上的以下方法, 对 ``.//`` 部分的解析是不同的. 一个
是相对于 root element, 另一个是相对于 current element.

- ``find_element_by_xpath()``

- ``find_elements_by_xpath()``

selector
^^^^^^^^
- ``find_element_by_css_selector()``

- ``find_elements_by_css_selector()``

generic methods
^^^^^^^^^^^^^^^
- ``find_element(by="id", value=None)``

- ``find_elements(by="id", value=None)``

- 这些方法实现了上述具体 APIs, 通过 ``selenium.webdriver.common.by.By`` class.

By
^^
- ``selenium.webdriver.common.by.By``.

design pattern
--------------
- Which one to choose when selecting a element:
  
  * focusing first on simple locators, then CSS, and leveraging XPath only when
    you need it (e.g. walking up the DOM).

  * Choose CSS selector and XPath when you need to ensure element hierarchy.

- use innerHTML/outerHTML virtual attribute to test text in source.

  .. code:: python

    text in element.get_property("innerHTML")

- 不要检测过细致的内容. 只进行功能点存在或生效方面的检测.

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

WebDriverWait
^^^^^^^^^^^^^
constructor
"""""""""""
- ``driver``.

- ``timeout``. max waiting time before raising timeout.

- ``poll_frequency=0.5``.

- ``ignored_exceptions=None``. a iterable of additional exceptions to be
  ignored during conditional polling. default is NoSuchElementException.

methods
"""""""
- ``until(method, message="")``. wait unitl method's return value is truthy.
  return method's value or raise TimeoutException.

- ``until_not(method, message="")``. wait until method's return value is falsy
  or one of the ignored exceptions is raised.  return method's value or True
  (if ignored exception raised), or raise TimeoutException.

expected conditions
^^^^^^^^^^^^^^^^^^^

python
""""""
- protocol: A expected condition is a callable that:

  * accepts a ``WebDriver`` instance.

  * returns False when the condition is not satisfied.

- definition: any simple function, a function that returns a function, a class
  instance that is callable.

- predefined expected conditions: ``selenium.webdriver.support.exepcted_conditions``

window
~~~~~~
- ``new_window_is_opened(current_handles)``. checking new window is opened
  after this condition is instantiated.

- ``number_of_windows_to_be(num)``. check the number of windows to be num.

title
~~~~~
- ``title_is(text)``. exact match.

- ``title_contains(text)``. page's title contains text.

url
~~~
- ``url_to_be(url)``. exact match.

- ``url_contains(text)``. driver's url contains text.

- ``url_matches(pattern)``. url match pattern by ``re.search()``.

- ``url_changes(url)``. check driver's current url changes from url.

presence
~~~~~~~~
Presence does not mean visibility.

- ``presence_of_element_located(locator)``. An element is present.

- ``presence_of_all_elements_located(locator)``. At least one element can
  be located by locator.

visibility
~~~~~~~~~~
Visibility means that the element is not only displayed but also has a height
and width that is greater than 0.

- ``visibility_of_element_located(locator)``. visible.

- ``visibility_of(element)``. visible.

- ``visibility_of_any_elements_located(locator)``. any element is visible.

- ``visibility_of_all_elements_located(locator)``. all elements are visible.

- ``invisibility_of_element_located(locator)``. element is either invisible
  or not present in DOM.

text
~~~~
- ``text_to_be_present_in_element(locator, text)``.

- ``text_to_be_present_in_element_value(locator, text)``. text in element's
  value attribute.

frame
~~~~~
- ``frame_to_be_available_and_switch_to_it(locator)``. check frame is available
  and switch to it if so.

click
~~~~~
- ``element_to_be_clickable(locator)``.

stale
~~~~~
- ``staleness_of(element)``. Wait until an element is no longer attached to the
  DOM.

selection
~~~~~~~~~
- ``element_to_be_selected(element)``. The element is selected. element is a
  WebElement.

- ``element_located_to_be_selected(locator)``. the located element is selected.

- ``element_selection_state_to_be(element, is_selected)``. element is a
  WebElement.

- ``element_located_selection_state_to_be(locator, is_selected)``.
  condition is element located by ``locator`` (``by, locator``) must be
  selected/unselected based on ``is_selected``.

alert
~~~~~
- ``alert_is_present()``

implicit waits
--------------
- Apply an overall polling mechanism when trying to find any element (or
  elements) not immediately available.

- 避免使用 implicit wait, 因为指定何时需要等待、何时不需要等待这属于程序
  行为定义的一部分. 是需要检测的.

- ``WebDriver.implicitly_wait(seconds)``

design patterns
---------------
- Explicit waits 用于将浏览器的异步操作转换为同步. 即 selenium 控制端 poll 浏览
  器的状态.

utilities
=========

keys
----
- python: ``selenium.webdriver.common.keys``

Keys
^^^^
- Constants for special keys.

actions
-------
- python: ``selenium.webdriver.common.action_chains``

ActionChains
^^^^^^^^^^^^
- a way to automate low level interactions such as mouse movements, mouse
  button actions, key press, and context menu interactions. 

- useful for doing complex actions.

- Actions are queued in ActionChains object until ``perform()`` is called.

- operation methods can be chained. All of them return the ActionChains object
  itself.

constructor
"""""""""""
- ``driver``. the browser driver to perform actions.

operations
""""""""""
- ``click(on_element=None)``. Click an element. if None, click the current mouse
  position.

- ``click_and_hold(on_element=None)``.

- ``context_click(on_element=None)``. right click.

- ``double_click(on_element=None)``.

- ``drag_and_drop(source, target)``. drag source to target.

- ``drag_and_drop_by_offset(source, xoffset, yoffset)``. drag source to the
  offset location.

- ``key_down(value, element=None)``. send key-down to the element, without
  releasing it. If element is None, send to currently focused element.
  Useful for control key.

- ``key_up(value, element=None)``. release it.

- ``send_keys(*keys)``. send keys to current focused element.

- ``send_keys_to_element(element, *keys)``. send keys to element.

- ``move_by_offset(xoffset, yoffset)``. move mouse by offset.

- ``move_to_element(to_element)``. move mouse to the middle of an element.

- ``move_to_element_with_offset(to_element, xoffset, yoffset)``. move mouse to
  element, by offset relative to the top-left corner of the element.

- ``pause(seconds)``. an operation that idles for the specified seconds.

- ``release(on_element=None)``. Releasing a held mouse button on an element.

apis
""""
- ``perform()``.

- ``reset_actions()``. clear queued actions.

select
------

Select
^^^^^^
- convenient manipulation for ``<select>``.

constructor
""""""""""""
- ``webelement``

attributes
""""""""""
- ``first_selected_option``.

- ``all_selected_options``.

- ``options``. all options.

methods
""""""""
- ``deselect_all()``. only valid if element support multiple selection.

- ``select_by_index(index)``. by option's index property.

- ``deselect_by_index(index)``.

- ``select_by_value(value)``. by option's value.

- ``deselect_by_value(value)``.

- ``select_by_visible_text(text)``. by option's text.

- ``deselect_by_visible_text(text)``.

touch actions
-------------

TouchActions
^^^^^^^^^^^^
- works like ActionChains, for touch actions.

alerts
------

Alert
^^^^^
- browser alert manipulation.

attributes
""""""""""
- ``text``. get the text of the alert.

methods
"""""""
- ``accept()``. like press Ok.

- ``dismiss()``. like any dismiss.

- ``authenticate(username, password)``. 401 authentication dialog.

- ``send_keys(text)``. send text to alert.

proxy
-----
- proxy settings.

service
-------
- used to manage webdriver server.

application cache
-----------------

color conversion
----------------

Color
^^^^^

event firing and listening
--------------------------

EventFiringWebDriver
^^^^^^^^^^^^^^^^^^^^
- A webdriver wrapper that support calling event handlers before/after
  an operation.

- It has the same APIs as WebDriver.

- Whenever underlying WebDriver returns WebElement, this instance returns
  EventFiringWebElement.

constructor
"""""""""""
- ``driver``.

- ``event_listener``. An object whose methods are handlers of events of
  interest.

attributes
""""""""""
- ``wrapped_driver``.

EventFiringWebElement
^^^^^^^^^^^^^^^^^^^^^
- Wrapper around WebElement, supporting firing event.

constructor
""""""""""""
- ``webelement``.

- ``ef_driver``. event firing webdriver.

attributes
""""""""""
- ``wrapped_element``.

AbstractEventListener
^^^^^^^^^^^^^^^^^^^^^
- subclass should implement one or many event handler methods of this ABC.

misc utils
----------
- misc internal utils.

exceptions
==========
python
------
module: ``selenium.common.exceptions``

- WebDriverException. base web driver exception.

desired capabilities
====================
- for interacting with remote webdriver.

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

