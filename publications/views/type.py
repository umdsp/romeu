__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from operator import itemgetter, attrgetter
from django.shortcuts import render_to_response
from django.template import RequestContext
from publications.models import Type, Publication

def type(request, pub_type=None):
	types, publications = [],[]
	years_for_type = set()
	year_issue = ()
	if pub_type:
		tablas_type_id = Type.objects.filter(type=pub_type)
		if tablas_type_id:
			publications = Publication.objects.filter(
				type_id=tablas_type_id[0].id, external=False
				).order_by('-year', '-number')
	else:
		publications = Publication.objects.filter(
			external=False
			).order_byorder_by('-year', '-number')

	for publication in publications:
		if publication.type.hidden:
			continue
		year_issue = (publication.year, publication.number.strip(' '))
		years_for_type.add(year_issue)
	a_list = list(years_for_type)
	list_of_years = sorted(a_list, key=lambda year: year, reverse=True)

	return render_to_response('publications/types.html',
							  {'pub_type':pub_type,
							   'years_for_type':list_of_years 
							   },
							  context_instance=RequestContext(request))
