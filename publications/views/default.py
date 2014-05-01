__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.shortcuts import render_to_response
from django.template import RequestContext
from publications.models import Type, Publication
from django.contrib.auth.decorators import login_required

@login_required
def default(request):
	types = []
	type_qs = Type.objects.filter(hidden=False,
								  owned_by_library=True).order_by('type')
	for type in type_qs:
		if Publication.objects.filter(type_id=type.id, external=False).exists():
			types.append(type)

	return render_to_response('publications/default.html', {
			'types': types
		}, context_instance=RequestContext(request))
