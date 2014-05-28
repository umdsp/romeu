from django.conf.urls import patterns, include, url
from views import *
from django.views.generic import TemplateView

urlpatterns = patterns('',
					   
	url(r'login/', accounts_login,  name='accounts_login'),
	url(r'logout/', accounts_logout, name='accounts_logout'),
	url(r'register/', accounts_register,  name="accounts_register"),
	url(r'change-password/', change_password, name='accounts_change_password'),
	url(r'request-new-password/', request_new_password,
		name='accounts_request_new_password'),
	url(r'reset-password/(?P<reset_password_key>[^/]+)/$', reset_password,
		name='accounts_reset_password'),
#	url(r'signup-verify/(?P<signup_key>[^/]+)/$', signup_verify,
#		name='accounts_signup_verify'),
	
	)
