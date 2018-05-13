from django import forms
from django.core import validators


class NullCharField(forms.CharField):
    """
    An alternative CharField that:

    - does not treat empty string as the same as None.

    - uses None as its empty value, rather than empty string.
    """

    empty_values = [*validators.EMPTY_VALUES]
    try:
        empty_values.remove("")
    except ValueError:
        pass

    def __init__(self, *, **kwargs):
        """
        The same signature as ``django.forms.CharField`` except that
        ``empty_value`` is ignored.
        """
        kwargs['empty_value'] = None
        super().__init__(**kwargs)
