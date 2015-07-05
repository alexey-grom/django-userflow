# encoding: utf-8

from django.utils.six import wraps


def if_new_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not kwargs.get('is_new', False):
            return
        user = kwargs.get('user', None)
        if not user:
            return
        return func(*args, **kwargs)
    return wrapper
