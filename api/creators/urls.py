from django.conf.urls import patterns, url
from django.conf.urls import include

from rest_framework.urlpatterns import format_suffix_patterns
from api.creators import views

urlpatterns = patterns('',

	url(r'^api/creators/$', 
		views.creator_api_view),
	url(r'^api/creators/all/(?P<lang>[\w\s\W]+)/$',
		views.CreatorsList.as_view(),
		name="api_creator_list_view"),
	url(r'^api/creators/(?P<pk>[0-9]+)/(?P<lang>[\w\s\W]+)/$',
		views.CreatorDetail.as_view(),
		name="api_creator_detail_view"),
	url(r'^api/creators/(?P<alpha>[\w\s\W]+)/(?P<lang>[\w\s\W]+)/$',
		views.CreatorAlphaDetail.as_view(),
		name="api_creator_alpha_view"),

)

urlpatterns = format_suffix_patterns(urlpatterns)

# Login and logout views for the browsable API
urlpatterns += patterns('',    
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
)