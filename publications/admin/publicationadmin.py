__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.contrib import admin
from publications.models import CustomLink, CustomFile
from archive.models import Creator, Production, WorkRecord
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

class CustomLinkInline(admin.StackedInline):
	model = CustomLink
	extra = 1
	max_num = 5


class CustomFileInline(admin.StackedInline):
	model = CustomFile
	extra = 1
	max_num = 5

class CreatorsInLine(admin.StackedInline):
	model = Creator.primary_publications.through
	verbose_name_plural = _('Primary Publication - Creator Relationships')
	extra = 0

class ProductionsInLine(admin.StackedInline):
	model = Production.primary_publications.through
	ordering = ['production__title']
	verbose_name_plural = _('Primary Publication - Production Relationships')
	extra = 0
	
class WorkRecordInLine(admin.StackedInline):
	model = WorkRecord.primary_publications.through
	verbose_name_plural = _('Primary Publication - WorkRecords Relationships')
	ordering = ['workrecord__title']
	extra = 0

class SecondaryCreatorsInLine(admin.StackedInline):
	model = Creator.secondary_publications.through
	verbose_name_plural = _('Secondary Publication - Creator Relationships')
	extra = 0

class SecondaryProductionsInLine(admin.StackedInline):
	model = Production.secondary_publications.through
	ordering = ['production__title']
	verbose_name_plural = _('Secondary Publication - Production Relationships')
	extra = 0
	
class SecondaryWorkRecordInLine(admin.StackedInline):
	model = WorkRecord.secondary_publications.through
	ordering = ['workrecord__title']
	verbose_name_plural = _('Secondary Publication - WorkRecords Relationships')
	extra = 0

class PublicationAdmin(admin.ModelAdmin):
	list_display = ('type', 'first_author', 'title',  'year',
					'journal_or_book_title')
	list_display_links = ('title',)
	change_list_template = 'admin/publications/change_list.html'
	search_fields = ('title', 'journal', 'authors', 'keywords', 'year')
	fieldsets = (
		('BibTex Standard fields', {
			'fields': ('type', 'title', 'authors', ('year', 'pub_date'),
					   'citekey', ('season', 'journal'),
					   ('volume', 'number'),
					   ('access_date', 'medium'),
					   'url', 'pdf', 'code',
					   ('book_title', 'chapter', 'pages'),
					   ('editor','address', 'publisher'),
					   ('series', 'series_num', 'series_text'),
					   ('edition', 'isbn', 'issn', 'doi'))
			}),
		(None, {
				'fields': (('translator', 'section'), 'prologue')
			}),
		(None, {
				'fields': ('note','extra')
			}),
		(None, {
			'fields': (('archive', 'archive_location'),
						'keywords')
			}),
		(None, {
			'fields': ('art_size', 'label',
					   'runtime', 'version')
			}),
		(None, {
			'fields': ('annote', 'organization',
					   'university', 'how_published',
					   'institution')
			}),
		(None, {
			'fields': ('price', 'rights', 'language',
					   'system', 'library',
					   'library_catalog_num', 'external')
			}),
	)
	inlines = [CreatorsInLine, SecondaryCreatorsInLine,
			   ProductionsInLine, SecondaryProductionsInLine,
			   WorkRecordInLine, SecondaryWorkRecordInLine,
			   CustomLinkInline, CustomFileInline]
	
	class Media:
		js = ('/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',)


