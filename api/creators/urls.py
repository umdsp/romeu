from django.conf.urls import patterns, url
from django.conf.urls import include

from rest_framework.urlpatterns import format_suffix_patterns
from api.creators import views

urlpatterns = patterns('',

	url(r'^api/creators/(?P<pk>[0-9]+)/$', views.CreatorDetail.as_view()),
	url(r'^api/creators/(?P<alpha>[\w\s\W]+)/$', views.CreatorAlphaDetail.as_view()),
	url(r'^api/creators/$', views.CreatorsList.as_view()),

)

urlpatterns = format_suffix_patterns(urlpatterns)

# Login and logout views for the browsable API
urlpatterns += patterns('',    
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
)