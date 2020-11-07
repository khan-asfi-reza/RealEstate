from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from Accounts.models import Owner, Location
from Provider.Location.models import Location
from Provider.RentDayProvider.models import Feature

# Create your models here.
# Features of a property
User = get_user_model()


# Property


class Property(models.Model):
    # Agent of this property
    agent = models.ForeignKey(to=User,
                              on_delete=models.SET_NULL,
                              blank=True,
                              related_name='agent_of_property',
                              verbose_name='Property Agent',
                              null=True)
    # Owner of the property
    owner = models.ForeignKey(to=Owner,
                              on_delete=models.SET_NULL,
                              blank=True,
                              related_name='owner_of_property',
                              verbose_name='Property Owner',
                              null=True
                              )
    # Property name
    name = models.CharField(max_length=256,
                            verbose_name='Property Name',
                            blank=True, null=True)

    # Property description
    description = models.TextField(max_length=512,
                                   verbose_name='Property Description',
                                   blank=True, null=True)

    # bathroom/bedroom/kitchen/living area number
    bathrooms = models.PositiveIntegerField(verbose_name='Number of bathroom', blank=True, null=True)
    bedrooms = models.PositiveIntegerField(verbose_name='Number of bedroom', blank=True, null=True)
    kitchen = models.PositiveIntegerField(verbose_name='Number of kitchen', blank=True, null=True)
    living_area = models.PositiveSmallIntegerField(verbose_name='Number of LivingArea', blank=True, null=True)
    rent = models.PositiveIntegerField(verbose_name='Property Rent', blank=True, null=True)
    parking_spot = models.PositiveSmallIntegerField(verbose_name='Parking Spot Type', blank=True, null=True,
                                                    choices=((1, 'Street Parking'),
                                                             (2, 'Garage Parking'),
                                                             (3, 'Undercover Parking')))
    parking_number = models.PositiveSmallIntegerField(blank=True, null=True)
    land_size = models.PositiveIntegerField(verbose_name='Size of land', blank=True, null=True)
    indoor_size = models.PositiveIntegerField(verbose_name='Size of indoor', blank=True, null=True)
    # Geo Location and address
    location = models.ForeignKey(to=Location, on_delete=models.CASCADE, blank=True, null=True)
    # Lease Length
    lease_length = models.PositiveIntegerField(blank=True, null=True)
    date_available = models.DateField(blank=True, null=True)
    # Property Features
    features = models.ManyToManyField(to=Feature, related_name='Property_Feature', blank=True)

    # Property Type
    property_type_choice = ((1, 'Apartment'), (2, 'House'), (3, 'Room'))
    property_type = models.PositiveSmallIntegerField(choices=property_type_choice, null=True)

    # walkthrough and plan
    walkthrough = models.FileField(blank=True, verbose_name='Property walkthrough', null=True)
    floor_plan = models.FileField(blank=True, verbose_name='Property FloorPlan', null=True)

    posted = models.DateTimeField(default=timezone.now, verbose_name='Posted On', null=True)

    # Methods of this function

    def get_agent_name(self):
        return "Property Does Not Have Agent" if self.agent is None else self.agent.get_full_name()

    def get_owner_name(self):
        return "Property Owner Not Available" if self.owner is None else self.owner.user.get_full_name()


# Images of a property
class Property_Images(models.Model):
    property = models.ForeignKey(to=Property,
                                 on_delete=models.CASCADE,
                                 verbose_name='Image of property',
                                 related_name='property_image')
    image_name = models.CharField(max_length=64, blank=True)
    image = models.ImageField()
    image_type = models.IntegerField(choices=((1, 'Interior'), (2, 'Exterior')), verbose_name="Property Image Type")


# Videos of a property
class Property_Video(models.Model):
    property = models.ForeignKey(to=Property,
                                 on_delete=models.CASCADE,
                                 verbose_name='Image of property',
                                 related_name='property_video')
    video_name = models.CharField(max_length=64)
    video = models.FileField()
