__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.shortcuts import render_to_response
from django.template import RequestContext
from publications.models import Type, Publication

def type(request, type=None):
	types = []
	if type:
		tablas_type_id = Type.objects.filter(type=type)
		publications = Publication.objects.filter(type_id=tablas_type_id[0].id, external=False)
	else:
		publications = Publication.objects.filter(external=False)
	publications = publications.order_by('type', '-year', 'authors', '-id')

	for publication in publications:
		if publication.type.hidden:
			continue
		if not types or (types[-1][0] != publication.type):
			types.append((publication.type, []))
		types[-1][1].append(publication)

	if 'ascii' in request.GET:
		return render_to_response('publications/publications.txt', {
				'publications': sum([y[1] for y in types], [])
			}, context_instance=RequestContext(request), mimetype='text/plain; charset=UTF-8')

	elif 'bibtex' in request.GET:
		return render_to_response('publications/publications.bib', {
				'publications': sum([y[1] for y in types], [])
			}, context_instance=RequestContext(request), mimetype='text/x-bibtex; charset=UTF-8')

	elif 'rss' in request.GET:
		return render_to_response('publications/publications.rss', {
				'url': 'http://' + request.META['HTTP_HOST'] + request.path,
				'publications': sum([y[1] for y in types], [])
			}, context_instance=RequestContext(request), mimetype='application/rss+xml; charset=UTF-8')

	else:
		for publication in publications:
			publication.links = publication.customlink_set.all()
			publication.files = publication.customfile_set.all()

		return render_to_response('publications/types.html', {
				'types': types
			}, context_instance=RequestContext(request))
