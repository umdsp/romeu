__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^$', 'publications.views.year'),
	url(r'^(?P<publication_id>\d+)/$', 'publications.views.id',
		name='publications_views_id'),
	url(r'^year/(?P<year>\d+)/$', 'publications.views.year',
		name='publications_view_year'),
	url(r'^tag/(?P<keyword>.+)/$', 'publications.views.keyword',
		name='publications_views_keyword'),
	url(r'^(?P<name>.+)/$', 'publications.views.person',
		name='publications_views_person'),
)