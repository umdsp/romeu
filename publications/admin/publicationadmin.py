__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.contrib import admin
from publications.models import CustomLink, CustomFile
from archive.models import Creator, Production, WorkRecord
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _


from publications.admin import forms as pubForms

class CustomLinkInline(admin.StackedInline):
	model = CustomLink
	extra = 1
	max_num = 5


class CustomFileInline(admin.StackedInline):
	model = CustomFile
	extra = 1
	max_num = 5


class PublicationAdmin(admin.ModelAdmin):
	
	form = pubForms.PublicationAdminForm
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
		('Relationships', {
			'fields': ('primary_creators', 'secondary_creators',
					   'primary_productions','secondary_productions',
					   'primary_workrecords','secondary_workrecords'
					   )
			}),
		
	)
	inlines = [CustomLinkInline, CustomFileInline]

	def save_related(self, request, form, formsets, change):

		publication = form.save()
		primary_creators = form.cleaned_data['primary_creators']
		secondary_creators = form.cleaned_data['secondary_creators']
		primary_productions = form.cleaned_data['primary_productions']
		secondary_productions = form.cleaned_data['secondary_productions']
		primary_workrecords = form.cleaned_data['primary_workrecords']
		secondary_workrecords = form.cleaned_data['secondary_workrecords']
		
		try:
			Creator.primary_publications.through.objects.filter(
				publication__id=publication.pk).delete()
			Creator.secondary_publications.through.objects.filter(
				publication__id=publication.pk).delete()
			Production.primary_publications.through.objects.filter(
				publication__id=publication.pk).delete()
			Production.secondary_publications.through.objects.filter(
				publication__id=publication.pk).delete()
			WorkRecord.primary_publications.through.objects.filter(
				publication__id=publication.pk).delete()
			WorkRecord.secondary_publications.through.objects.filter(
				publication__id=publication.pk).delete()
	
			for pc in primary_creators:
				pc.primary_publications.add(publication)
			for sc in secondary_creators:
				sc.secondary_publications.add(publication)		
			for pp in primary_productions:
				pp.primary_publications.add(publication)
			for sp in secondary_productions:
				sp.secondary_publications.add(publication)
			for wp in primary_workrecords:
				wp.primary_publications.add(publication)
			for ws in secondary_workrecords:
				ws.secondary_publications.add(publication)
		except:
			pass
			
		return super(PublicationAdmin, self).save_related(request, form, formsets, change)
	

	class Media:
		js = ('/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',)


