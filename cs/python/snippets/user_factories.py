import factory
from factory.django import DjangoModelFactory

from django.conf import settings


class UserFactory(DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Faker("user_name")
    password = factory.Faker("password")
    email = factory.Faker("ascii_safe_email")
    real_name = factory.Faker("name", locale="zh_CN")
    is_superuser = False
    is_staff = False
    is_active = True

    @factory.post_generation
    def hash_password(obj, create, extracted, **kwargs):
        """
        Convert raw password to password hash.

        Raw password is stored as `_raw_password`, for testing
        use. Because the password is generated randomly, we
        don't known actual password beforehand.
        """
        obj._raw_password = raw_password = obj.password
        obj.set_password(raw_password)
        # If create strategy is used, also save password hash
        # to database
        if create:
            obj.save()
