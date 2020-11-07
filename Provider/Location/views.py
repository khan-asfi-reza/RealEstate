from rest_framework import status
# Create your views here.
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from Provider.Location.models import Location
from .serializers import LocationSerializer


class LocationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get(self, request, **kwargs):
        # if there is a data in request data then show that data or else show all

        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Post Request View
    def post(self, request, format=None):
        # Serializer of Location
        serializer = LocationSerializer(data=request.data)
        # if serializer is valid it will save it and return a response
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Otherwise it will return errors and a bad request
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    # Put Request View
    def put(self, request, format=None):
        # id request data
        id = request.data['id']
        # location serializer
        serializer = LocationSerializer(id, data=request.data)
        # If serializer is valid it will save
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # Otherwise it will show error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
