# encoding: utf-8

from django.conf.urls import url, include, patterns

from userflow import views


urlpatterns = patterns('',
    url(r'^', include([
        url('^signin/', views.signin.SigninView.as_view(), name='signin'),
        url('^signup/', views.signup.SignupView.as_view(), name='signup'),
        url('^signout/$', views.signout.SignoutView.as_view(), name='signout'),
    ], namespace='users')),
)
