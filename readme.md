Features
========

* email as primary auth credential
* flexible sign(in/up/out) flow by **pipelines** *(like python-social-auth)*
* customizable user model
* multiple emails
* mailing
* optional confirm emails and restore accounts
* optional build-in profile page and users top
* and a lot of other stuff


Pipelines
=========

Composition of actions:

```
USERS_FLOW_UP = ('userflow.pipeline.activation.activate_by_default',
                 'userflow.pipeline.auth.signup',
                 'userflow.pipeline.mails.signup_email',
                 'userflow.pipeline.auth.signin',
                 'userflow.pipeline.redirects.next_redirect',
                 'userflow.pipeline.redirects.login_redirect', )
USERS_FLOW_DOWN = ('userflow.pipeline.auth.signout',
                   'userflow.pipeline.redirects.next_redirect',
                   'userflow.pipeline.redirects.index_redirect', )
```

Custom action signature:

```
def pipeline_action(request, user=None, is_new=None, data=None, **kwargs):
    # dict for update kwargs
    if is_new:
        return {
            'new data': 'to pipeline',
        }

    # or response
    elif user:
        return HttpResponse()

    # or none
    # pass
```


Build-in actions
================

- Sign

    * `userflow.pipeline.auth.signup`
    * `userflow.pipeline.auth.signin`
    * `userflow.pipeline.auth.signout`

- Account activation

    * `userflow.pipeline.activation.active_by_default`
    * `userflow.pipeline.activation.activate_by_email_verify`

- Mails

    * `userflow.pipeline.mails.signup_email`
    * `userflow.pipeline.mails.email_verify`

- Redirects

    * `userflow.pipeline.redirects.next_redirect` redirect to ?next=… if it present
    * `userflow.pipeline.redirects.index_redirect` redirect to /
    * `userflow.pipeline.redirects.login_redirect` redirect to `settings.LOGIN_REDIRECT_URL`


Generic flow
============

- (default) User not activated after signup; account activation by email confirm 

```
USERS_FLOW_UP = (
    'userflow.pipeline.auth.signup',
    'userflow.pipeline.mails.signup_email',
    'userflow.pipeline.activation.activate_by_email_confirm',
    'userflow.pipeline.auth.signin',
    'userflow.pipeline.redirects.next_redirect',
    'userflow.pipeline.redirects.login_redirect',
)
```

- User activated after signup; signin; optional mail confirm email

```
USERS_FLOW_UP = (
    'userflow.pipeline.activation.activate_by_default',
    'userflow.pipeline.auth.signup',
    'userflow.pipeline.mails.signup_email',
    'userflow.pipeline.mails.email_verify',
    'userflow.pipeline.auth.signin',
    'userflow.pipeline.redirects.next_redirect',
    'userflow.pipeline.redirects.login_redirect',
)
```


Settings
========

* Pipelines

    - `USERS_FLOW_UP`
    - `USERS_FLOW_DOWN`

* Forms

    - `USERS_SIGNUP_FORM`
    - `USERS_SIGNIN_FORM`

* Mailing

    - `USERS_SITE_URL`
    - `USERS_SITE_NAME`
    - `USERS_DUMMY_EMAIL`

Quick start
===========

* Install app

* Inherit user model `yourapp/models.py`

```
from userflow.models import BaseUser, UserInfoMixin

class User(UserInfoMixin, BaseUser):
    pass
```

* `settings.py`

```
INSTALLED_APPS += ('userflow', )
AUTH_USER_MODEL = 'yourapp.User' 
```

* `urls.py`

```
url(r'^', include('userflow.urls')),  # or your urls composition 
```
