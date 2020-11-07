# RestFramework Imports
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from idna import unicode
from rest_auth.registration.views import SocialLoginView
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.http import JsonResponse
import json
# Account app imports
from rest_framework.views import APIView

from Accounts.permissions import (IsPostOrIsAuthenticated,
                                  AgentPermission,
                                  RenterPermission)
from .models import (Renter,
                     Renter_Property_Pref,
                     Renter_Property_Pref_Location,
                     Agent,
                     Agency,
                     Owner)
from .serializers import (OwnerSerializer,
                          AuthenticationSerializer,
                          RenterSerializer,
                          RenterPropertyPrefSerializer,
                          RenterPropertyPrefLocationSerializer,
                          AgentSerializer,
                          AgencySerializer,
                          ChangePasswordSerializer,
                          UserSerializer)

# Getting Our User Model
User = get_user_model()

"""
Reusable Account Class View
"""


class AccountClassView(viewsets.ModelViewSet):
    # Adding Authentication classes Token Authentication
    # Allow only TokenAuthentication, will be changed according to other views
    authentication_classes = [TokenAuthentication]
    # Permissions only authenticated users
    permission_classes = [IsAuthenticated]
    # Gives JSON Rendered Class
    renderer_classes = [JSONRenderer]
    # Serializer Class for this Class View, Have to set in class views
    serializer_class = None
    # Query set of all renter objects
    queryset = None
    # Query Object
    queryobject = None

    # get detail view to request user
    @action(methods=['get'], detail=True)
    def retrieve(self, request, pk=None):
        # Getting instance
        instance = get_object_or_404(self.queryset, user=request.user)
        # Instance serializer
        serializer = self.get_serializer(instance, many=False)
        # return serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)

    # post view to request user allow post request
    @action(methods=['post'], detail=True)
    def create(self, request):
        # giving serializer the data from request data
        serializer = self.get_serializer(data=request.data)
        # checks if serializer is valid
        if serializer.is_valid():
            # saves user information
            serializer.save(user=request.user)
            # Return data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Otherwise it will return errors and a bad request
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    # Put method request view for updating information
    @action(methods=['put'], detail=True)
    def update(self, request):
        # Renter Serializer
        instance = self.queryobject.get(user=request.user)
        serializer = self.get_serializer(instance=instance, data=request.data)
        # If serializer is valid it will save
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Otherwise it will show error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Add other necessary methods for view


# User Create View for api/accounts/
class UserCreate(AccountClassView):
    # Changing permission class to Post or Authenticate, Allow Post request if user is not authenticated
    permission_classes = []
    # user serializer
    serializer_class = UserSerializer
    # Query set of all user objects
    queryset = User.objects.all()
    # Query Object of user
    queryobject = User.objects

    @action(methods=['delete'], detail=False)
    def destroy(self, request, *args, **kwargs):
        objectDelete = self.queryobject.get(request.user)
        objectDelete.delete()
        return Response('User Successfully Deleted', status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def create(self, request):
        # giving serializer the data from request data
        serializer = self.get_serializer(data=request.data)
        # checks if serializer is valid
        if serializer.is_valid():
            # saves user information
            user = serializer.save(user=request.user)
            # Return data
            token, created = Token.objects.get_or_create(user=user)
            new_data = {'token': token.key}
            new_data.update(serializer.data)
            # return new token
            return Response(new_data, status=status.HTTP_200_OK)

        # Otherwise it will return errors and a bad request
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=True)
    def update(self, request):
        # Renter Serializer
        instance = self.queryobject.get(email=request.user)
        serializer = self.get_serializer(instance=instance, data=request.data)
        # If serializer is valid it will save
        if serializer.is_valid():
            user = serializer.save()
            oldToken = Token.objects.get(user=user)
            oldToken.delete()
            token, created = Token.objects.get_or_create(user=user)
            new_data = {'token': token.key}
            new_data.update(serializer.data)
            # return new token
            return Response(new_data, status=status.HTTP_200_OK)
        # Otherwise it will show error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True)
    def retrieve(self, request, pk=None):
        # Getting instance
        instance = get_object_or_404(self.queryset, email=request.user)
        # Instance serializer
        serializer = self.get_serializer(instance, many=False)
        # return serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)


# Change user password
class PasswordChangeView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    # user serializer
    serializer_class = ChangePasswordSerializer
    # Query set of all user objects
    queryset = User.objects.all()
    # Query Object of user
    queryobject = User.objects

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def update_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # if using drf auth token, create a new token
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        token, created = Token.objects.get_or_create(user=user)
        # return new token
        return Response({'token': token.key}, status=status.HTTP_200_OK)


# Token VIEW for users token authentication
class CreateTokenView(APIView):
    serializer_class = AuthenticationSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        userObject = User.objects.get(email=user)
        us = UserSerializer(userObject)
        content = {
            'token': unicode(token.key),
            'user': us.data
        }

        return Response(content)



# Google Login View
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


"""
This following segment manages Renter Model View

"""


# Renter View for Renter Profile

class RenterView(AccountClassView):
    # Permissions only allow renters and authenticated users
    permission_classes = [IsAuthenticated]
    # Serializer Class for this Class View (Renter)
    serializer_class = RenterSerializer
    # Query set of all renter objects
    queryset = Renter.objects.all()
    queryobject = Renter.objects


# Renter View for Renter Preferences

class RenterPrefView(AccountClassView):
    # Serializer Class for this Class View (Renter Property Preferances)
    permission_classes = [IsAuthenticated, RenterPermission]
    serializer_class = RenterPropertyPrefSerializer
    # Query set of all renter objects
    queryset = Renter_Property_Pref.objects.all()
    # Query Object for Renter Property Pref
    queryobject = Renter_Property_Pref.objects


# Renter Pref Location Create View

class RenterPrefLocationView(AccountClassView):
    # Permissions only allow renters and authenticated users
    permission_classes = [IsAuthenticated, RenterPermission]
    # Serializer Class for this Class View (renter pref locations )
    serializer_class = RenterPropertyPrefLocationSerializer
    # Query set of all renter pref locations objects
    queryset = Renter_Property_Pref_Location.objects.all()
    # Query Object
    queryobject = Renter_Property_Pref_Location.objects


"""

This following section manages agent related view
Model - Agent Model and agent related model

"""


class AgentView(AccountClassView):
    # Permissions only allow renters and authenticated users
    permission_classes = [IsAuthenticated]
    # Serializer Class for this Class View (Agent)
    serializer_class = AgentSerializer
    # Query set of all agent objects
    queryset = Agent.objects.all()
    # Query Object
    queryobject = Agent.objects


class AgencyView(AccountClassView):
    permission_classes = [IsAuthenticated]
    # Serializer Class for this Class View
    serializer_class = AgencySerializer
    # Query set of all renter objects
    queryset = Agency.objects.all()
    # Query Object
    queryobject = Agency.objects


"""

This segment manages Owner view
Model > Owner

"""


class OwnerView(AccountClassView):
    permission_classes = [IsAuthenticated]
    # Serializer Class for this Class View
    serializer_class = OwnerSerializer
    # Query set of all renter objects
    queryset = Owner.objects.all()
    # Query Object
    queryobject = Owner.objects


class TestAuth(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self,request):
        return Response("Response", status=status.HTTP_200_OK)


@csrf_exempt
def emailAvailablity(request):
    if request.method == 'POST':
        print(request.POST.get('email', False))
        if User.objects.filter(email=request.POST['email']).exists():
            return JsonResponse({'available': '0'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'available': '1'}, status=status.HTTP_200_OK)

    else:
        return JsonResponse({'available': '-1'}, status=status.HTTP_200_OK)

