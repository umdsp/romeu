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
		return HttpResponseRedirect(
			reverse('api_creator_list_view', args=(lang,)))	
	
	return render(request, 'creators_api.html')


