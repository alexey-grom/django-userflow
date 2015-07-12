# encoding: utf-8

from hashlib import md5

from django.utils.http import urlencode


class Gravatar(object):
    FORMAT = 'http://www.gravatar.com/avatar/{hash}{file_ext}?{options}'

    def __init__(self, email, **options):
        """
        https://ru.gravatar.com/site/implement/images/
        :param user:
        :param rating:
        :param file_ext:
        :param size:
        :param default:
        """

        self.email = email

        self.size = None
        self.file_ext = None
        self.default = None
        self.rating = None

        for key, value in options.items():
            if not hasattr(self, key):
                continue
            setattr(self, key, value)

    def _get_email_hash(self):
        """
        https://gravatar.com/site/implement/hash/
        """
        email_hash = md5()
        email_hash.update(self.email.encode('utf-8'))
        return email_hash.hexdigest()

    def get_url(self):
        return self.FORMAT.format(hash=self._get_email_hash(),
                                  file_ext=self.file_ext or '',
                                  options=urlencode(self.get_options()))

    def get_options(self):
        result = {
            's': self.size or '',
            'd': self.default or '',
            'r': self.rating or '',
        }
        return result

    @property
    def url(self):
        return self.get_url()
