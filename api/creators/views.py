from archive.models import Creator
from api.creators.serializers import CreatorSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, XMLRenderer


class CreatorList(APIView):
	"""
	List all creators, or create a new snippet.
	"""

	renderer_classes = (JSONRenderer, XMLRenderer)
	
	def get(self, request, format=None):
		creators = Creator.objects.all()
		serializer = CreatorSerializer(creators, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = CreatorSerializer(data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatorDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    renderer_classes = (JSONRenderer, XMLRenderer)

    def get_object(self, pk):
        try:
            return Creator.objects.get(pk=pk)
        except Creator.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        creator = self.get_object(pk)
        serializer = CreatorSerializer(creator)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        creator = self.get_object(pk)
        serializer = CreatorSerializer(creator, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        creator = self.get_object(pk)
#        creator.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)