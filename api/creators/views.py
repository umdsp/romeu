from django.http import Http404
from django.utils import translation
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, XMLRenderer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from archive.models import Creator, RelatedCreator
from api.creators.serializers import CreatorSerializer

class CreatorsList(APIView):

	"""
	List all creators,
	"""

#	authentication_classes = (SessionAuthentication, BasicAuthentication)
#	permission_classes = (IsAuthenticated,)
	renderer_classes = (XMLRenderer, JSONRenderer)
	
	def get(self, request, lang=None, format=None):
		if lang:
			translation.activate(lang)
		creators = Creator.objects.all()
		serializer = CreatorSerializer(creators, many=True)
		response = Response(serializer.data)
		if format == 'json':
			response['Content-Disposition'] = 'attachment; filename="creators.json"'
		else:
			response['Content-Disposition'] = 'attachment; filename="creators.xml"'
		return response
	

class CreatorDetail(APIView):
	
	"""
	Use a get to retrieve a creator instances
	using the pass in pk parameter
	"""
	
#	authentication_classes = (SessionAuthentication, BasicAuthentication)
#	permission_classes = (IsAuthenticated,)
	renderer_classes = (XMLRenderer, JSONRenderer)

	greeting = "Good Day"
	
	def get_object(self, pk):
		try:
			return Creator.objects.get(pk=pk)
		except Creator.DoesNotExist:
			raise Http404
	
	def get(self, request, pk, lang=None, format=None):
		if lang is not None:
			translation.activate(lang)

		creator = self.get_object(pk)
		serializer = CreatorSerializer(creator)
		response = Response(serializer.data)
		if format == 'json':
			response['Content-Disposition'] = 'attachment; filename="creators.json"'
		else:
			response['Content-Disposition'] = 'attachment; filename="creators.xml"'
		return response		

class CreatorAlphaDetail(APIView):
	"""
	Use a filter to retrieve all creator instances
	that match the alpha pass in parameter
	"""

#	authentication_classes = (SessionAuthentication, BasicAuthentication)
#	permission_classes = (IsAuthenticated,)
	renderer_classes = (XMLRenderer, JSONRenderer)
	
	def get_object(self, alpha):
		
		creators = Creator.objects.filter(family_name__icontains=alpha)
		if creators:
			return creators
		creators = Creator.objects.filter(org_name__icontains=alpha)
		if creators:
			return creators
		else:
			raise Http404
	
	def get(self, request, alpha, lang=None, format=None):
		if lang is not None:
			translation.activate(lang)
		creator = self.get_object(alpha)
		if creator.count() > 1:
			serializer = CreatorSerializer(creator)
		else:
			serializer = CreatorSerializer(creator, many=True)
		response = Response(serializer.data)
		if format == 'json':
			response['Content-Disposition'] = 'attachment; filename="creators.json"'
		else:
			response['Content-Disposition'] = 'attachment; filename="creators.xml"'
		return response


def creator_api_view(request):

	if request.POST:
		lang=request.POST.get('lang', '')
		creator_id = request.POST.get('creator', 0)
		if int(creator_id) > 0:
			return HttpResponseRedirect(
				reverse('api_creator_detail_view', args=(creator_id, lang,)))	
		else:	
			return HttpResponseRedirect(
				reverse('api_creator_list_view', args=(lang,)))
		
	creator_qs = Creator.objects.filter(published=True)
	return render(request, 'creators_api.html',
				  {"creator_list": creator_qs})


def update_progress_direct(request):
	
	"""
		Return JSON object with information about the progress of an upload.
	"""

	from django.core.cache import cache
	from django.http import HttpResponse, HttpResponseServerError 

	progress_id = ''
	if 'X-Progress-ID' in request.GET:
		progress_id = request.GET['X-Progress-ID']
	elif 'X-Progress-ID' in request.META:
		progress_id = request.META['X-Progress-ID']
	if progress_id:
		from django.utils import simplejson
		cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
		data = cache.get(cache_key)
		return HttpResponse(simplejson.dumps(data))
	else:
		return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')


def get_download_progress(request):
	
	from django.utils import simplejson
	from django.core.cache import cache
	cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], request.GET['X-Progress-ID'])
	data = cache.get(cache_key)
	return HttpResponse(simplejson.dumps(data))
