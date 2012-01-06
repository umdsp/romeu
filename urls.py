from django.conf.urls.defaults import *
from django.conf import settings

from archive.views import CreatorsListView, CreatorsAlphaListView, CreatorDetailView, \
                          ProductionsListView, ProductionsAlphaListView, ProductionDetailView, \
                          WorkRecordsListView, WorkRecordsAlphaListView, WorkRecordDetailView, \
                          VenuesListView, VenuesAlphaListView, VenueDetailView, \
                          DigitalObjectsListView, DigitalObjectDetailView, search_view, flatpage

DEFAULT_LANG = settings.DEFAULT_LANG

from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView, search_view_factory

from archive.views import flatpage

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

sqs = SearchQuerySet().order_by('django_ct')

DEFAULT_TEMPLATE = 'flatpages/default.html'

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^ctda/', include('ctda.foo.urls')),

    # static pages
    (r'^$', flatpage, {'url': '/'}),

    (r'^creators/?$', CreatorsListView.as_view()),
    (r'^creators/(?P<alpha>[a-z0]{1})/?$', CreatorsAlphaListView.as_view()),
    (r'^creator/(?P<pk>\d+)/?$', CreatorDetailView.as_view()),
    
    (r'^productions/?$', ProductionsListView.as_view()),
    (r'^productions/(?P<alpha>[a-z0]{1})/?$', ProductionsAlphaListView.as_view()),
    (r'^production/(?P<pk>\d+)/?$', ProductionDetailView.as_view()),
    
    (r'^writtenworks/?$', WorkRecordsListView.as_view()),
    (r'^writtenworks/(?P<alpha>[a-z0]{1})/?$', WorkRecordsAlphaListView.as_view()),
    (r'^writtenwork/(?P<pk>\d+)/?$', WorkRecordDetailView.as_view()),
    
    (r'^venues/?$', VenuesListView.as_view()),
    (r'^venues/(?P<alpha>[a-z0]{1})/?$', VenuesAlphaListView.as_view()),
    (r'^venue/(?P<pk>\d+)/?$', VenueDetailView.as_view()),
    
    (r'^digitalobjects/?$', DigitalObjectsListView.as_view()),
    (r'^digitalobject/(?P<pk>\d+)/?$', DigitalObjectDetailView.as_view()),
    
    # Set up i18n functions
    (r'^i18n/', include('django.conf.urls.i18n')),

    (r'^tinymce/', include('tinymce.urls')),

    (r'^ajax_select/', include('ajax_select.urls')),
    (r'^chaining/', include('smart_selects.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    (r'^search/', search_view),
    
    (r'^selectable/', include('selectable.urls')),
    
    # Static media
    #(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/kzurawel/webapps/ctda_media/js'}),
    #(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/kzurawel/webapps/ctda_media/css'}),
    #(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/kzurawel/webapps/ctda_media/images'}),
)

#urlpatterns += patterns('haystack.views',
#    url(r'^search/', search_view_factory(
#        view_class=SearchView,
#        form_class=ModelSearchForm,
#        searchqueryset=sqs
#    ), name='haystack_search'),
#)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )
