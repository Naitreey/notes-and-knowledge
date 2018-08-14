from django.db import models


class FriendlyDateTimeField(models.DateTimeField):
    """
    A DateTimeField that respects the explicitly set value without
    overriding it unconditionally. In other words, a DateTimeField
    that is friendly.

    The ability to set datetime value explicitly is necessary during
    unit test.
    """

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value:
            return value
        else:
            return super().pre_save(model_instance, add)
