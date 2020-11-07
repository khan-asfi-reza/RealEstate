# Rest Framework Imports

from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Property_Images, Property_Video, Property
# Property Imports
from .permissions import IsOwnerOrReadOnly, IsAgentOrIsOwner
from .serializers import ImageSerializer, VideoSerializer, PropertySerializer

# Media --> Images / Videos Media View --> Post and Get
"""
Reuseable Code

"""


class MediaCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAgentOrIsOwner]
    serializer_class = None
    media = None

    def modify_input_for_multiple_files(self, property_id, file, name):
        obj = {'property': property_id,
               f"{self.media}": file,
               f"{self.media}_name": name,
               }
        return obj

    def post(self, request, pk):
        property_id = pk
        # converts query dict to original dict
        media = dict(request.data.lists())[self.media]
        names = dict(request.data.lists())[f"{self.media}_name"]
        media_name_list = list(zip(media, names))
        print(media_name_list)
        flag = 1
        arr = []
        for element in media_name_list:
            modified_data = self.modify_input_for_multiple_files(property_id,
                                                                 element[0],
                                                                 element[1])
            file_serializer = self.serializer_class(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):

        images = Property_Images.objects.filter(property=pk)
        serializer = self.serializer_class(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MediaDetailView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [TokenAuthentication]
    serializer_class = None
    model = None

    def get(self, request, pk, prop):
        queryset = self.model.objects.get(property=prop, pk=pk)
        serializer = self.serializer_class(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk, prop):
        queryset = self.model.objects.get(property=prop, pk=pk)
        serializer = self.serializer_class(instance=queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk, prop):
        queryset = self.model.objects.get(property=prop, pk=pk)
        queryset.delete()
        return Response('Data deleted', status=status.HTTP_204_NO_CONTENT)


"""
Images and Videos for properties
"""


# Only post and get method image for property
class ImageView(MediaCreateView):
    serializer_class = ImageSerializer
    media = 'image'
    queryset = Property_Images.objects.all()
    queryobject = Property_Images.objects


# Only post and get method video for property
class VideoView(MediaCreateView):
    serializer_class = VideoSerializer
    media = 'video'
    queryset = Property_Video.objects.all()
    queryobject = Property_Video.objects


# Allow detail view --> Get,Update,Destroy Method of Images
class ImageDetailView(MediaDetailView):
    serializer_class = ImageSerializer
    model = Property_Images


# Allow detail view --> Get,Update,Destroy Method of Videos
class VideoDetailView(MediaDetailView):
    serializer_class = VideoSerializer
    model = Property_Video


"""
Property Views
"""


# Property View only post and get method --> list view
class PropertyView(viewsets.generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PropertySerializer
    queryset = Property.objects.all()


# Property crud detail view
class PropertyRetrieveUpdateDestroyView(viewsets.generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [TokenAuthentication]
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return self.queryset
