# encoding: utf-8

from django.conf import settings
from django.utils.html import format_html

TEMPLATE_PACK = getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap')


class Link(object):
    def __init__(self, url, title, css_classes=None, *args, **kwargs):
        self.url = url
        self.title = title
        self.css_classes = css_classes or ''

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        return format_html('<a class="{css_classes}" href="{url}">{title}</a>',
                           css_classes=self.css_classes,
                           url=self.url,
                           title=self.title)
