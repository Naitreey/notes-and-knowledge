"""
Browser Test Runner.

Use one browser session for all unit tests to speed up unit testing.

Additional settings:

- TEST_BROWSER_DRIVER
"""
from django.conf import settings
from django.test.runner import DiscoverRunner


_DRIVER_CLASS = None
_DRIVER = None


def set_driver_class(test_driver_class=None):
    global _DRIVER_CLASS
    test_driver_class = test_driver_class or settings.TEST_BROWSER_DRIVER
    driver_paths = test_driver_class.split(".")
    if len(driver_paths) > 1:
        driver_module_name = ".".join(driver_paths[:-1])
    else:
        driver_module_name = "."
    driver_module = __import__(
        driver_module_name,
        fromlist=(driver_paths[-1],)
    )
    _DRIVER_CLASS = getattr(driver_module, driver_paths[-1])


def get_browser_driver(*args, **kwargs):
    global _DRIVER_CLASS, _DRIVER
    if _DRIVER is None:
        _DRIVER = _DRIVER_CLASS(*args, **kwargs)
        return _DRIVER
    else:
        return _DRIVER


def quit_browser_driver():
    global _DRIVER
    if _DRIVER is not None:
        _DRIVER.quit()
        _DRIVER = None


class BrowserRunner(DiscoverRunner):

    def __init__(self, browserdriver=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.browserdriver = browserdriver

    @classmethod
    def add_arguments(cls, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--browserdriver", action="store", dest="browserdriver",
            help="Use specified browser driver class instead of the default "
                 "TEST_BROWSER_DRIVER setting.",
        )

    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)
        set_driver_class(self.browserdriver)

    def teardown_test_environment(self, **kwargs):
        super().teardown_test_environment(**kwargs)
        quit_browser_driver()
