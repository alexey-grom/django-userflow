# encoding: utf-8

from django.conf.urls import url, include, patterns
from django.views.generic.base import RedirectView

from userflow import views


sign_urls = patterns('',
    url('^signin/', views.sign.signin.SigninView.as_view(), name='signin'),
    url('^signup/', views.sign.signup.SignupView.as_view(), name='signup'),
    url('^signout/$', views.sign.signout.SignoutView.as_view(), name='signout'),
)

reset_urls = patterns('',
    url('^request/$', views.reset.request.PasswordResetView.as_view(), name='request'),
    url('^wait/(?P<pk>\d+)/(?P<key>[^/]+)/$', views.reset.wait.ResetWaitView.as_view(), name='wait'),
    url('^change/(?P<pk>\d+)/(?P<key>[^/]+)/$', views.reset.change.SetPasswordView.as_view(), name='confirm'),
)

verify_urls = patterns('',
    url('^confirm/(?P<pk>\d+)/(?P<key>[^/]+)/$', views.verify.confirm.ConfirmEmailView.as_view(), name='confirm'),
    url('^wait/(?P<pk>\d+)/(?P<key>[^/]+)/$', views.verify.wait.WaitConfirmEmailView.as_view(), name='wait'),
    url('^request/(?P<pk>\d+)/$', views.verify.request.RequestConfirmEmailView.as_view(), name='request'),
)

profile_view_urls = patterns('',
    url('^$', views.profile.user.UserProfileView.as_view(), name='view'),
    url('^(?P<pk>\d+)/$', views.profile.user.UserProfileView.as_view(), name='view'),
)

profile_edit_urls = patterns('',
    url(r'^$', views.profile.edit.PersonalEditView.as_view(), name='edit'),
    url(r'^(?P<name>personal)/$', views.profile.edit.PersonalEditView.as_view(), name='edit'),
    url(r'^(?P<name>about)/$', views.profile.edit.AboutEditView.as_view(), name='edit'),
    url(r'^(?P<name>password)/$', views.profile.edit.PasswordView.as_view(), name='edit'),
)

emails_urls = patterns('',
    url(r'^(?P<pk>\d+)/(?P<action>public|private)/$', views.profile.emails.public.PublicUpdateView.as_view(), name='public'),
    url(r'^(?P<pk>\d+)/primary/$', views.profile.emails.primary.PrimaryUpdateView.as_view(), name='primary'),
    url(r'^(?P<pk>\d+)/remove/$', views.profile.emails.remove.RemoveView.as_view(), name='remove'),
    url(r'^(?P<pk>\d+)/verify/$', views.profile.emails.verify.VerifyView.as_view(), name='verify'),
    url(r'^add/$', views.profile.emails.create.AddEmailView.as_view(), name='add'),
)

contacts_urls = patterns('',
    url(r'^(?P<pk>\d+)/remove/$', views.profile.contacts.remove.RemoveView.as_view(), name='remove'),
    url(r'^add/$', views.profile.contacts.create.AddContactView.as_view(), name='add'),
)

urlpatterns = patterns('',
    url(r'^', include(patterns('',
        url(r'^', include(sign_urls)),
        url(r'^reset/', include(reset_urls, namespace='reset')),
        url(r'^verify/', include(verify_urls, namespace='verify')),

        url(r'^profile/', include(patterns('',
            url(r'^', include(profile_view_urls)),
            url(r'^edit/', include(profile_edit_urls)),
            url(r'^emails/', include(emails_urls, namespace='emails')),
            url(r'contacts/', include(contacts_urls, namespace='contacts')),
        ), namespace='profile')),

        # url(r'rating/', include(patterns('',
        #     url(r'^$', RedirectView.as_view(url='/'), name='rating'),
        # ))),

    ), namespace='users')),
)
