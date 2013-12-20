__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from publications.bibtex import parse
from publications.models import Publication, Type
from archive.models import Creator, Production, WorkRecord

from string import split, join

# mapping of months
MONTHS = {
	'jan': 1, 'january': 1,
	'feb': 2, 'february': 2,
	'mar': 3, 'march': 3,
	'apr': 4, 'april': 4,
	'may': 5,
	'jun': 6, 'june': 6,
	'jul': 7, 'july': 7,
	'aug': 8, 'august': 8,
	'sep': 9, 'september': 9,
	'oct': 10, 'october': 10,
	'nov': 11, 'november': 11,
	'dec': 12, 'december': 12}

def import_bibtex(request):
	if request.method == 'POST':
		# try to parse BibTex
		the_bibtex_file_content = ''
		
		the_bibtex_file = request.FILES.get('bibtex_file', '')
		if the_bibtex_file:
			if the_bibtex_file.multiple_chunks():
				the_bibtex_file_content =  ''.join(chunk for chunk in the_bibtex_file.chunks())
			else:
				the_bibtex_file_content = the_bibtex_file.read()

		bib = parse(the_bibtex_file_content)

		if not bib:
			bib = parse(request.POST['bibliography'])
			
		# container for error messages
		errors = {}

		# publication types
		types = Type.objects.all()

		# check for errors
		if not bib:
			if not request.POST['bibliography']:
				errors['bibliography'] = 'Please populate Bibliography or click browse to upload a Bibtex format file.'

		if not errors:
			publications = []

			# try adding publications
			for entry in bib:
				if (entry.has_key('title') and 
				   entry.has_key('author') and 
				   entry.has_key('year')):

					# parse authors
					authors = split(entry['author'], ' and ')
					for i in range(len(authors)):
						author = split(authors[i], ',')
						author = [author[-1]] + author[:-1]
						authors[i] = join(author, ' ')
					authors = join(authors, ', ')

					# add missing keys
					keys = [
						'annote',
						'booktitle',
						'chapter',
						'edition',
						'editor',
						'howpublished',
						'institution',
						'journal',
						'key',
						'month',
						'note',
						'number',
						'organization',
						'pages',
						'publisher',
						'address',
						'school',
						'series',
						'volume',
						'issue',
						'url',
						'isbn',
						'issn',
						'lccn',
						'abstract',
						'keywords',
						'price',
						'copyright',
						'language',
						'contents',
						'doi']

					for key in keys:
						if not entry.has_key(key):
							if key == 'price':
								entry[key] = 0
							else:
								entry[key] = ''

					# map integer fields to integers
					entry['month'] = MONTHS.get(entry['month'].lower(), 0)
					entry['volume'] = entry.get('volume', None)
					entry['number'] = entry.get('number', None)

					# determine type
					type_id = None

					for t in types:
						if entry['type'] in t.bibtex_type_list:
							type_id = t.id
							break

					if type_id is None:
						errors['bibliography'] = 'Type "' + entry['type'] + '" unknown.'
						break

					# add publication
					publications.append(Publication(
						type_id=type_id,
						annote=entry['annote'],
						authors=authors,
						book_title=entry['booktitle'],
						chapter=entry['chapter'],
						edition=entry['edition'],
						editor=entry['editor'],
						how_published=entry['howpublished'],
						institution=entry['institution'],
						journal=entry['journal'],
						citekey=entry['key'],
						year=entry['year'],
						month=entry['month'],
						note=entry['note'],
						organization=entry['organization'],
						pages=entry['pages'],
						publisher=entry['publisher'],
						address=entry['address'],
						university=entry['school'],
						series=entry['series'],
						title=entry['title'],
						volume=entry['volume'],
						number=entry['issue'],
						url=entry['url'],
						isbn=entry['isbn'],
						issn=entry['issn'],
						archive_location=entry['lccn'],
						abstract=entry['abstract'],
						keywords=entry['keywords'],
						price=entry['price'],
						rights=entry['copyright'],
						language=entry['language'],
						table_of_content=entry['contents'],
						doi=entry['doi']))
				else:
					errors['bibliography'] = 'Make sure that the keys title, author and year are present.'
					break

		if not errors and not publications:
			errors['bibliography'] = 'No valid BibTex entries found.'

		if errors:
			# some error occurred
			return render_to_response(
				'admin/publications/import_bibtex.html', {
					'errors': errors,
					'title': 'Import BibTex',
					'types': Type.objects.all(),
					'request': request},
				RequestContext(request))
		else:
			try:
				# save publications
				creator_id = request.POST.get('creator_id', 0)
				production_id = request.POST.get('production_id', 0)
				work_record_id = request.POST.get('work_record_id', 0)

				for publication in publications:
					publication.save()
					try:
						creator = Creator.objects.get(pk=creator_id)
						creator.primary_publications.add(publication)
					except:
						pass
					try:
						production = Production.objects.get(pk=production_id)
						production.primary_publications.add(publication)
					except:
						pass
					try:
						work_record = WorkRecord.objects.get(pk=work_record_id)
						work_record.primary_publications.add(publication)
					except:
						pass
			except:
				msg = 'Some error occured during saving of publications.'
			else:
				if len(publications) > 1:
					msg = 'Successfully added ' + str(len(publications)) + ' publications.'
				else:
					msg = 'Successfully added ' + str(len(publications)) + ' publication.'

			# show message
			messages.info(request, msg)

			# redirect to publication listing
			return HttpResponseRedirect('../')
	else:
		Creators_qs = Creator.objects.all()
		Productions_qs = Production.objects.all()
		WorkRecord_qs = WorkRecord.objects.all()
		
		CREATOR_CHOICES = [("", "-- Select a Creator --")]
		CREATOR_CHOICES += [(e.id,
						 e.display_name())
						 for e in Creators_qs]

		PRODUCTION_CHOICES = [("", "-- Select a Production --")]
		PRODUCTION_CHOICES += [(e.id,
						 e.title)
						 for e in Productions_qs]
		
		WORKRECORD_CHOICES = [("", "-- Select a Written Work --")]
		WORKRECORD_CHOICES += [(e.id,
						 e.title)
						 for e in WorkRecord_qs]
			
		return render_to_response(
			'admin/publications/import_bibtex.html', {
				'title': 'Import BibTex',
				'types': Type.objects.all(),
				'creators': CREATOR_CHOICES,
				'productions': PRODUCTION_CHOICES,
				'work_records': WORKRECORD_CHOICES,
				'request': request},
			RequestContext(request))

import_bibtex = staff_member_required(import_bibtex)
