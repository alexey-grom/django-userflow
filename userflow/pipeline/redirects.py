# encoding: utf-8

from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.utils.http import is_safe_url


def next_redirect(request, **kwargs):
    redirect_to = request.GET.get('next')
    if not is_safe_url(url=redirect_to, host=request.get_host()):
        return
    return HttpResponseRedirect(redirect_to)


def login_redirect(request, **kwargs):
    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)


def index_redirect(request, **kwargs):
    return HttpResponseRedirect('/')
