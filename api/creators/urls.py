from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from api.creators import views

urlpatterns = patterns('',

	url(r'^api/creators/(?P<pk>[0-9]+)/$', views.CreatorDetail.as_view()),
	url(r'^api/creators/(?P<alpha>[\w\s\W]+)/$', views.CreatorAlphaDetail.as_view()),
	url(r'^api/creators/$', views.CreatorsList.as_view()),

)

urlpatterns = format_suffix_patterns(urlpatterns)