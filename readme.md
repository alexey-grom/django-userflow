Features
========

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

    USERS_FLOW_UP = ('userflow.pipeline.defaults.active_by_default',
                     'userflow.pipeline.auth.signup',
                     'userflow.pipeline.mails.signup_email',
                     'userflow.pipeline.auth.signin',
                     'userflow.pipeline.redirects.next_redirect',
                     'userflow.pipeline.redirects.login_redirect', )
    USERS_FLOW_DOWN = ('userflow.pipeline.auth.signout',
                       'userflow.pipeline.redirects.next_redirect',
                       'userflow.pipeline.redirects.index_redirect', )

Custom action signature:

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


Build-in actions
================

- Sign

    * `userflow.pipeline.auth.signup`
    * `userflow.pipeline.auth.signin`
    * `userflow.pipeline.auth.signout`

- Account activation

    * `userflow.pipeline.defaults.active_by_default`
    * `userflow.pipeline.emails.activate_by_email_verify`

- Redirects

    * `userflow.pipeline.redirects.next_redirect` redirect to ?next=… if it present
    * `userflow.pipeline.redirects.index_redirect` redirect to /
    * `userflow.pipeline.redirects.login_redirect` redirect to `settings.LOGIN_REDIRECT_URL`


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

1. Install app
1. `settings.py`

```
AUTH_USER_MODEL = 'userflow.User'  # or your inheritor
```

1. `urls.py`

```
url(r'^', include('userflow.urls')),
```
