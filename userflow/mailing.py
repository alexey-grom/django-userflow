# encoding: utf-8

from django.conf import settings
from django.core.mail import send_mail as _send_mail
from django.template.loader import render_to_string


__all__ = 'send_mail',


def send_mail(to, email_template, request=None, context=None):
    from userflow import conf

    template_context = {
        'site_url': conf.get_site_url(request),
        'site_name': conf.get_site_name(request),
    }
    template_context.update(context or {})

    template = lambda frmt: frmt.format(email_template)
    render = lambda frmt: render_to_string(template(frmt),
                                           template_context)

    _send_mail(
        render('userflow/emails/{}-subject.txt').strip(),
        render('userflow/emails/{}.txt'),
        settings.SERVER_EMAIL,
        [to],
        fail_silently=False,
        html_message=render('userflow/emails/{}.html')
    )
