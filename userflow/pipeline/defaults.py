# encoding: utf-8


def defaults(request, is_new=False, data=None, **kwargs):
    if not is_new or not data:
        return
    data.update({
        'is_active': True,
    })
