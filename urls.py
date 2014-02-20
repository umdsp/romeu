# Copyright (C) 2012  University of Miami
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from django.conf.urls import patterns, url, include
from django.conf import settings

from archive.views import (CreatorsListView, CreatorsAlphaListView,
                           CreatorDetailView, ProductionsListView,
                           ProductionsAlphaListView, ProductionDetailView,
                           WorkRecordsListView, WorkRecordsAlphaListView,
                           WorkRecordDetailView, FestivalsListView,
                           FestivalsAlphaListView, FestivalDetailView,
                           FestivalOccurrenceDetailView,
                           VenuesListView, VenuesAlphaListView,
                           VenueDetailView, DigitalObjectsListView,
                           DigitalObjectDetailView, search_view,
                           search_do_view, scalar_search_view,
                           flatpage, DigitalObjectsVideosListView,
                           DigitalObjectsImagesListView, collections_list,
                           DigitalObjectsTypeListView, phys_types_list,
                           DigitalObjectsCollectionListView,
                           AwardsListView, AwardsAlphaListView,
                           AwardDetailView, TaggedItemsListView, TaggedItemDetailView,
                           )

DEFAULT_LANG = settings.DEFAULT_LANG

from haystack.forms import ModelSearchForm, FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView, search_view_factory, FacetedSearchView

from archive.views import flatpage, get_creators_json_response, get_creators_org_name_json_response

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

sqs = SearchQuerySet().order_by('django_ct')

DEFAULT_TEMPLATE = 'flatpages/default.html'

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # static pages
    url(r'^$', flatpage, {'url': '/'}),

    url(r'^creators/?$', CreatorsListView.as_view(),
        name="creator_list_view"),
    url(r'^creators/(?P<alpha>[a-z0]{1})/?$', CreatorsAlphaListView.as_view(),
        name="creator_alpha_list_view"),
    url(r'^creator/(?P<pk>\d+)/?$', CreatorDetailView.as_view(),
        name="creator_detail_view"),
    
    url(r'^productions/?$', ProductionsListView.as_view(),
        name="production_list_view"),
    url(r'^productions/(?P<alpha>[a-z0]{1})/?$', ProductionsAlphaListView.as_view(),
        name="production_alpha_list_view"),
    url(r'^production/(?P<pk>\d+)/?$', ProductionDetailView.as_view(),
        name="production_detail_view"),
    
    url(r'^writtenworks/?$', WorkRecordsListView.as_view(),
        name="workrecord_list_view"),
    url(r'^writtenworks/(?P<alpha>[a-z0]{1})/?$',
        WorkRecordsAlphaListView.as_view(),
        name="workrecord_alpha_list_view"),
    url(r'^writtenwork/(?P<pk>\d+)/?$', WorkRecordDetailView.as_view(),
        name="workrecord_detail_view"),
    
    url(r'^venues/?$', VenuesListView.as_view(),
        name="venue_list_view"),
    url(r'^venues/(?P<alpha>[a-z0]{1})/?$',
        VenuesAlphaListView.as_view(),
        name="venue_alpha_list_view"),
    url(r'^venue/(?P<pk>\d+)/?$', VenueDetailView.as_view(),
        name="venue_detail_view"),
    
    url(r'^digitalobjects/?$',
        DigitalObjectsListView.as_view(),
        name="digital_object_list_view"),
    url(r'^digitalobjects/videos/?$',
        DigitalObjectsVideosListView.as_view(),
        name="digital_object_video_list_view"),
    url(r'^digitalobjects/images/?$',
        DigitalObjectsImagesListView.as_view(),
        name="digital_object_image_list_view"),
    url(r'^digitalobjects/types/?$', phys_types_list,
        name="digital_object_type"),
    url(r'^digitalobjects/type/(\S+)/?$',
        DigitalObjectsTypeListView.as_view(),
        name="digital_object_type_list_view"),
    url(r'^digitalobjects/collections/?$',
        collections_list,
        name="digital_object_collection"),
    url(r'^digitalobjects/collection/(\S+)/?$',
        DigitalObjectsCollectionListView.as_view(),
        name="digital_object_collection_list_view"),
    url(r'^digitalobject/(?P<pk>\d+)/?$',
        DigitalObjectDetailView.as_view(),
        name="digital_object_detail_view"),

    url(r'^festivals/?$', FestivalsListView.as_view(),
        name="festivals_list_view"),
    url(r'^festivals/(?P<alpha>[a-z0]{1})/?$',
        FestivalsAlphaListView.as_view(),
        name="festivals_alpha_list_view"),
    url(r'^festival/(?P<pk>\d+)/?$', FestivalDetailView.as_view(),
        name="festival_detail_view"),
    url(r'^festival/Occurrence/(?P<pk>\d+)/?$', FestivalOccurrenceDetailView.as_view(),
        name="festival_occurrence_detail_view"),
    
    url(r'^awards/?$', AwardsListView.as_view(),
        name="awards_list_view"),
    url(r'^awards/(?P<alpha>[a-z0]{1})/?$',
        AwardsAlphaListView.as_view(),
        name="awards_alpha_list_view"),
    url(r'^award/(?P<pk>\d+)/?$', AwardDetailView.as_view(),
        name="award_detail_view"),
    
    # Set up i18n functions
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^tinymce/', include('tinymce.urls')),

    url(r'^ajax_select/', include('ajax_select.urls')),
    url(r'^chaining/', include('smart_selects.urls')),

    url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    
    url(r'^publications/', include('publications.urls')),
    url(r'^admin/publications/publication/import_bibtex/$', 'publications.admin_views.import_bibtex'),
    url(r'^admin/publications/type/import_bibtex/$', 'publications.admin_views.import_bibtex'),

    url(r'^ajax/creators/$',
          'archive.views.get_creators_json_response', name='ajax_get_creators_in_json'),
    url(r'^ajax/creators/org_name/$',
          'archive.views.get_creators_org_name_json_response', name='ajax_get_creators_org_name_in_json'),    
     
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^search/', search_view),
    
    url(r'^selectable/', include('selectable.urls')),
    url(r'^objsearch/', scalar_search_view),

    url(r'^taggit_autocomplete_modified/', include('taggit_autocomplete_modified.urls')),

    url(r'^search_do/', search_do_view),

    url(r'^taggeditems/?$', TaggedItemsListView.as_view(),
        name="taggeditems_list_view"),
    url(r'^taggeditem/(?P<pk>\d+)/?$', TaggedItemDetailView.as_view(),
        name="taggeditem_detail_view"),
    )

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )
    
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
    urlpatterns += patterns('', url(r'^media/(.*)$', 'django.views.static.serve', kwargs={'document_root': settings.MEDIA_ROOT }), )

