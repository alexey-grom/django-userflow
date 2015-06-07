# encoding: utf-8

from django.contrib.sites.models import get_current_site


def dummy_site_url(request=None):
    protocol = 'http'
    domain = get_current_site(request).domain
    if request and request.is_secure():
        protocol = 'https'
    return '{protocol}://{domain}'.format(domain=domain,
                                          protocol=protocol)


def dummy_site_name(request=None):
    current_site = get_current_site(request)
    return current_site.name or \
           current_site.domain
