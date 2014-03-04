__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.contrib import admin
from publications.models import CustomLink, CustomFile
from archive.models import Creator, Production, WorkRecord

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
	extra = 0

class ProductionsInLine(admin.StackedInline):
	class Meta:
		ordering = ['title']
	model = Production.primary_publications.through
	extra = 0
	
class WorkRecordInLine(admin.StackedInline):
	model = WorkRecord.primary_publications.through
	extra = 0
	
class PublicationAdmin(admin.ModelAdmin):
	list_display = ('type', 'first_author', 'title',  'year', 'journal_or_book_title')
	list_display_links = ('title',)
	change_list_template = 'admin/publications/change_list.html'
	search_fields = ('title', 'journal', 'authors', 'keywords', 'year')
	fieldsets = (
		('BibTex Standard fields', {'fields': 
			('type', 'title', 'authors', ('year', 'month'),
			 'citekey', 'annote', ('book_title', 'edition', 'chapter', 'pages', 'isbn', 'issn', 'doi'),
			 'editor', 'publisher', 'address', 'how_published',
			'institution', 'volume',
			'journal',
			'note',
			'number',
			'organization',
			'university',
			('series', 'series_text', 'series_num'),
			'url',
			('archive', 'archive_location'),
			'abstract',
			'keywords',
			'price',
			'rights',
			'language',
			)
			}),
		(None, {'fields': 
			('translator', 'section', 'pub_date')}),
		(None, {'fields': 
			('access_date', 'medium', 'art_size', 'label', 'runtime')}),
		(None, {'fields': 
			('version', 'system', 'library', 'library_catalog_num', 'extra')}),		
		(None, {'fields': 
			('code', 'pdf', 'external')}),
	)
	inlines = [CreatorsInLine, ProductionsInLine, WorkRecordInLine, CustomLinkInline, CustomFileInline]


