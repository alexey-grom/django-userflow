# encoding: utf-8

from social.apps.django_app.default.models import DjangoStorage, UserSocialAuth
from userflow.models.emails import UserEmail


class UserSocialAuthProxy(UserSocialAuth):
    @classmethod
    def get_users_by_email(cls, email):
        return cls.user_model().objects.\
            filter(emails__email__iexact=email)

    @classmethod
    def user_exists(cls, *args, **kwargs):
        return cls.user_model().objects.\
            filter(emails__email=kwargs.pop('username')).\
            exists()

    @classmethod
    def create_user(cls, *args, **kwargs):
        from pprint import pprint
        pprint([args, kwargs])

        username = kwargs.pop('username')
        user = cls.user_model().objects.\
            create_user(name=username,
                        *args, **kwargs)
        return user

    @classmethod
    def username_field(cls):
        raise NotImplementedError

    @classmethod
    def username_max_length(cls):
        return 30

    @classmethod
    def get_username(cls, user):
        return user.id

    class Meta:
        proxy = True
        app_label = 'default'


class UserflowStorage(DjangoStorage):
    user = UserSocialAuthProxy
    user_email = UserEmail
