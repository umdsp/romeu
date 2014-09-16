__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.shortcuts import render_to_response
from django.template import RequestContext
from publications.models import Type, Publication

def year(request, pub_type=None, year=None, issue=None):

	if issue is None:
		if request.GET.get('issue'):
			issue = request.GET['issue']
	years = []
	publications = Publication.objects.filter(external=False)
	if pub_type:
		tablas_type_id = Type.objects.filter(type=pub_type)
		if tablas_type_id:
			publications = publications.filter(type_id=tablas_type_id[0].id)
	if year:
		publications = publications.filter(year=year)
	if issue:
		publications = publications.filter(number__contains=issue)

	publications = publications.order_by('-year', '-number', '-id')

	for publication in publications:
		if publication.type.hidden:
			continue
		if not years or (years[-1][0] != publication.year):
			years.append((publication.year, []))
		years[-1][1].append(publication)

	if 'ascii' in request.GET:
		return render_to_response('publications/publications.txt', {
				'publications': sum([y[1] for y in years], [])
			}, context_instance=RequestContext(request), mimetype='text/plain; charset=UTF-8')

	elif 'bibtex' in request.GET:
		return render_to_response('publications/publications.bib', {
				'publications': sum([y[1] for y in years], [])
			}, context_instance=RequestContext(request), mimetype='text/x-bibtex; charset=UTF-8')

	elif 'rss' in request.GET:
		return render_to_response('publications/publications.rss', {
				'url': 'http://' + request.META['HTTP_HOST'] + request.path,
				'publications': sum([y[1] for y in years], [])
			}, context_instance=RequestContext(request), mimetype='application/rss+xml; charset=UTF-8')

	else:
		for publication in publications:
			publication.links = publication.customlink_set.all()
			publication.files = publication.customfile_set.all()
		return render_to_response('publications/years.html', {
				'years': years,
				'issue':issue
			}, context_instance=RequestContext(request))
