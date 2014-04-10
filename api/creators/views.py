from archive.models import Creator, RelatedCreator
from api.creators.serializers import CreatorSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, XMLRenderer
from rest_framework.decorators import api_view


class CreatorsList(APIView):
	"""
	List all creators,
	"""

	renderer_classes = (XMLRenderer, JSONRenderer)
	
	def get(self, request, format=None):
		creators = Creator.objects.all()
		serializer = CreatorSerializer(creators, many=True)
		return Response(serializer.data)


class CreatorDetail(APIView):
	"""
	Retrieve a creator instance.
	"""
	renderer_classes = (XMLRenderer, JSONRenderer)
	
	def get_object(self, pk):
		try:
			return Creator.objects.get(pk=pk)
		except Creator.DoesNotExist:
			raise Http404
	
	def get(self, request, pk, format=None):
		creator = self.get_object(pk)
		serializer = CreatorSerializer(creator)
		return Response(serializer.data)

class CreatorAlphaDetail(APIView):
	"""
	Retrieve a creator instance.
	"""
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
	
	def get(self, request, alpha, format=None):
		creator = self.get_object(alpha)
		if creator.count() > 1:
			serializer = CreatorSerializer(creator)
		else:
			serializer = CreatorSerializer(creator, many=True)
		return Response(serializer.data)




