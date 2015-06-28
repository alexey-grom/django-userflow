# encoding: utf-8

from django.conf.urls import url, include, patterns
from django.views.generic.base import RedirectView

from userflow import views


urlpatterns = patterns('',
    url(r'^', include([
        url(r'^', include([
            url('^signin/', views.sign.signin.SigninView.as_view(), name='signin'),
            url('^signup/', views.sign.signup.SignupView.as_view(), name='signup'),
            url('^signout/$', views.sign.signout.SignoutView.as_view(), name='signout'),
        ])),

        url(r'^reset/', include([
            url('^request/$', views.reset.request.PasswordResetView.as_view(), name='request'),
            url('^wait/(?P<pk>\d+)/(?P<key>[^/]+)/$', views.reset.wait.ResetWaitView.as_view(), name='wait'),
            url('^change/(?P<pk>\d+)/(?P<key>[^/]+)/$', views.reset.change.SetPasswordView.as_view(), name='confirm'),
        ], namespace='reset')),

        url(r'^verify/', include([
            url('^confirm/(?P<pk>\d+)/(?P<key>[^/]+)/$', views.verify.confirm.ConfirmEmailView.as_view(), name='confirm'),
            url('^wait/(?P<pk>\d+)/(?P<key>[^/]+)/$', views.verify.wait.WaitConfirmEmailView.as_view(), name='wait'),
            url('^request/(?P<pk>\d+)/$', views.verify.request.RequestConfirmEmailView.as_view(), name='request'),
        ], namespace='verify')),

        url(r'^profile/', include([
            url('^$', views.profile.user.UserProfileView.as_view(), name='profile'),
            url('^(?P<pk>\d+)/$', views.profile.user.UserProfileView.as_view(), name='profile'),

            url(r'edit/', include([
                url(r'^$', views.profile.edit.PersonalEditView.as_view(), name='edit'),
                url(r'^(?P<name>personal)/$', views.profile.edit.PersonalEditView.as_view(), name='edit'),
                url(r'^(?P<name>about)/$', views.profile.edit.AboutEditView.as_view(), name='edit'),
                url(r'^(?P<name>password)/$', views.profile.edit.PasswordView.as_view(), name='edit'),
                url(r'^(?P<name>emails)/$', views.profile.edit.EmailsEditView.as_view(), name='edit'),
                url(r'^(?P<name>contacts)/$', views.profile.edit.ContactsEditView.as_view(), name='edit'),
            ])),

        ])),

        url(r'rating/', include([
            url(r'^$', RedirectView.as_view(url='/'), name='rating'),
        ])),

    ], namespace='users')),
)
