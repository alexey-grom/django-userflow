# encoding: utf-8

from django.conf.urls import url, include, patterns

from userflow import views


urlpatterns = patterns('',
    url(r'^', include([
        url(r'^', include([
            url('^signin/', views.sign.signin.SigninView.as_view(), name='signin'),
            url('^signup/', views.sign.signup.SignupView.as_view(), name='signup'),
            url('^signout/$', views.sign.signout.SignoutView.as_view(), name='signout'),
        ])),
        url(r'^reset/', include([
            url('^request/$', views.reset.request.PasswordResetView.as_view(), name='reset-password'),
            url('^wait/$', views.reset.wait.ResetWaitView.as_view(), name='reset-wait'),
            url('^change/(?P<pk>\d+)/(?P<key>[^/]+)/$', views.reset.change.SetPasswordView.as_view(), name='set-password'),
        ])),
        url(r'^verify/', include([
            url('^confirm/(?P<pk>\d+)/(?P<key>[^/]+)/$', views.verify.confirm.ConfirmEmailView.as_view(), name='verify-confirm'),
            url('^wait/(?P<pk>\d+)/(?P<key>[^/]+)/$', views.verify.wait.WaitConfirmEmailView.as_view(), name='verify-wait'),
            url('^request/(?P<pk>\d+)/$', views.verify.request.RequestConfirmEmailView.as_view(), name='verify-request'),
        ])),
        url(r'^profile/', include([
            url('^$', views.reset.request.PasswordResetView.as_view(), name='user'),
            url('^edit/$', views.reset.request.PasswordResetView.as_view(), name='edit'),
            url('^(?P<pk>\d+)/$', views.reset.request.PasswordResetView.as_view(), name='user'),
            url('^(?P<email>[^/]+)/$', views.reset.request.PasswordResetView.as_view(), name='user'),
        ])),
    ], namespace='users')),
)
