from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from .models import *

# Serializers define the API representation.


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator])


    class Meta:
        model = User
        fields = ['id','email', 'password', 'account_type', 'first_name', 'last_name', 'verified']
        read_only_fields = ['id','verified']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def validated_email(self, value):
        qs = User.objects.filter(email=self.instance.email)
        if self.instance:
            qs = qs.exclude(email=self.instance.email)
            if qs.exists():
                raise serializers.ValidationError("Email is already used")
        return value

    def create(self, validated_data):
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError('Email already exists')
        user = User.objects.create_user(email=validated_data['email'],
                                        password=validated_data['password'],
                                        account_type=validated_data['account_type'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'])


        return user

    def update(self, instance, validated_data):
        if instance.email != validated_data['email']:
            instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


# Authentication token serializer
class AuthenticationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True)
    password = serializers.CharField(required=True,
                                     style={'input_type': 'password'},
                                     trim_whitespace=False)

    def validate(self, attrs):
        # Validate and authenticate
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'),
                            username=email,
                            password=password)
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError({'error':msg}, code='authentication')

        attrs['user'] = user
        return attrs


# Renter Profile Serializer
class RenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Renter
        fields = ['id', 'gender', 'status', 'occupation', 'date_of_birth', 'income', 'income_pre_tax',
                  'people_living_with', 'marital_status', 'phone_number', 'profile_photo']
        read_only_fields = ['id']


# Renter Property Preferences Profile Serializer
class RenterPropertyPrefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Renter_Property_Pref
        fields = ['id', 'property_type', 'bathrooms', 'bedrooms', 'parking_spot', 'move_in', 'suburb',
                  'min_price', 'max_price', 'location']
        read_only_fields = ['id']


# Renter Property Pref Location
class RenterPropertyPrefLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Renter_Property_Pref_Location
        fields = ['id', 'office_type', 'office_location', 'custom_location', 'custom_location_2', 'desibel_rating']
        read_only_fields = ['id']


# Renter Agent Profile Serializer
class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'gender', 'phone_number', 'date_of_birth', 'agency', 'licence', 'suburbs',
                  'profile_photo']
        read_only_fields = ['id']


# Renter Agency Profile Serializer
class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ['name', 'location']


# Owner Profile Serializer
class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['property_license', 'profile_photo']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True, trim_whitespace=False)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True, trim_whitespace=False)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Your old password was entered incorrectly. Please enter it again.')
            )
        return value

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user
