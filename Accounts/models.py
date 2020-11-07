from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models

from Accounts.manager import UserManager
from Provider.Location.models import Location

phone_error_message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits Allowed"
# custom user class/ model

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        editable=True
    )
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    # is the user active or not
    active = models.BooleanField(default=True)
    # a admin user; non super-user
    staff = models.BooleanField(default=False)
    # a superuser
    admin = models.BooleanField(default=False)
    # If user is Renter/Agent/Admin
    role_choice = ((1, 'Renter'), (2, 'Agent'), (3, 'Admin'))
    account_type = models.PositiveSmallIntegerField(choices=role_choice, default=1, null=True)

    # If user is verified
    verified = models.BooleanField(default=False)

    # Default username field is removed and current username field is email field
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    # calling usermanager class
    objects = UserManager()

    def get_full_name(self):
        # Return user's full name
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        # Return user's last name
        return self.email

    def get_username(self):
        # return user's email without their domain
        return str(f"{self.email.split('@')[0]}")

    def has_perm(self, perm, obj=None):
        # User permission to view
        return True

    def has_module_perms(self, app_label):
        # User permission to view

        return True

    def __str__(self):
        # Return string object of email
        return self.email

    @property
    def is_staff(self):
        # Returns true if user is staff
        return self.staff

    @property
    def is_admin(self):
        # returns true if user is admin or not
        return self.admin

    @property
    def is_active(self):
        # returns true if user is active or not
        return self.active

    @property
    def is_renter(self):
        # returns true if user is active or not
        return self.account_type == 1

    @property
    def is_agent(self):
        # returns true if user is active or not
        return self.account_type == 2


user_model = get_user_model()


class Renter(models.Model):
    # Renter pointed to the main user
    user = models.OneToOneField(to=user_model,
                                on_delete=models.CASCADE,
                                limit_choices_to={'account_type': 1})

    # Gender choice
    gender_choice = ((1, 'Male'), (2, 'Female'), (3, 'Others'))
    gender = models.PositiveSmallIntegerField(choices=gender_choice,
                                              blank=True)
    # Student/Worker/Businessman choice
    status_choice = ((1, 'Student'), (2, 'Worker'), (3, 'Businessman'))
    status = models.PositiveSmallIntegerField(choices=status_choice,
                                              blank=True)
    # Occupation ,date of birth and income
    occupation = models.CharField(max_length=64,
                                  blank=True)

    date_of_birth = models.DateField(blank=True,
                                     null=True)

    income = models.PositiveIntegerField(blank=True)

    income_pre_tax = models.PositiveIntegerField(blank=True)
    # Family
    people_living_with = models.PositiveSmallIntegerField(blank=True)
    marital_choice = ((1, 'Married'), (2, 'Unmarried'))
    marital_status = models.PositiveSmallIntegerField(choices=marital_choice, blank=True)
    # Phone number and phone number validator
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message=phone_error_message, )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    profile_photo = models.ImageField(blank=True, default='default.jpg')

    # returns string
    def __str__(self):
        return self.user.email

    # returns renters email address
    def get_renter_username(self):
        return self.user.email


class Renter_Property_Pref(models.Model):
    # The Renter
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, limit_choices_to={'account_type': 1})
    # The property type looking for
    property_type_choice = ((1, 'Apartment'), (2, 'House'), (3, 'Room'))
    property_type = models.PositiveSmallIntegerField(blank=True, choices=property_type_choice)
    # Number of rooms/areas
    bathrooms = models.PositiveIntegerField(blank=True)
    bedrooms = models.PositiveIntegerField(blank=True)
    parking_spot = models.PositiveIntegerField(blank=True)
    # Time of moving in
    move_in = models.DateField(blank=True)
    # Places (Update Later)
    suburb = models.ManyToManyField(to=Location,blank=True, related_name='Renter_Suburb_Wants')
    # Price Range
    min_price = models.IntegerField(blank=True)
    max_price = models.IntegerField(blank=True)
    # Location
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.email

    def get_renter_username(self):
        return self.user.email


class Renter_Property_Pref_Location(models.Model):
    # Renter user
    renter = models.OneToOneField(to=User, on_delete=models.CASCADE, limit_choices_to={'account_type': 1})
    # Where does the renter work from
    office_type = models.PositiveSmallIntegerField(default=1,
                                                   verbose_name='Work From',
                                                   choices=((1, 'Office'), (2, 'Home'))
                                                   )
    # Renter office Location
    office_location = models.ForeignKey(Location,
                                        on_delete=models.SET_NULL,
                                        null=True,
                                        verbose_name='Office Location',
                                        related_name="renter_office_location")
    custom_location = models.ForeignKey(Location,
                                        on_delete=models.SET_NULL,
                                        null=True,
                                        verbose_name='Custom Location 1',
                                        related_name="renter_custom_location")
    custom_location_2 = models.ForeignKey(Location,
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          verbose_name='Custom Location 2',
                                          related_name="renter_custom2_location2")
    desibel_rating = models.DecimalField(max_digits=8, decimal_places=6)

    def __str__(self):
        return self.renter.email

    def get_renter_username(self):
        return self.renter.email


# Agency Of an Agent
class Agency(models.Model):
    name = models.CharField(max_length=256)
    Location = models.ForeignKey(to=Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Agent(models.Model):
    # user account
    user = models.ForeignKey(to=user_model, on_delete=models.CASCADE, related_name='agent',
                             limit_choices_to={'account_type': 2})
    # gender
    gender_choice = ((1, 'Male'), (2, 'Female'), (3, 'Others'))
    gender = models.PositiveSmallIntegerField(choices=gender_choice, blank=True)
    # agent phone number
    phone_number = models.CharField(max_length=14)
    # date of birth
    date_of_birth = models.DateField()
    # agency name
    agency = models.ForeignKey(to=Agency,
                               blank=True,
                               on_delete=models.SET_NULL,
                               related_name='agent_under_the_agency',
                               null=True)
    # realstate licence
    licence = models.CharField(max_length=128, verbose_name='RealState Licence')
    suburbs = models.ManyToManyField(to=Location, blank=True, verbose_name='Suburbs Properties Available')
    profile_photo = models.ImageField(blank=True, default='default.jpg')

    def __str__(self):
        return self.user.email

    def get_renter_username(self):
        return self.user.email


class Owner(models.Model):
    # Owner / user
    user = models.ForeignKey(to=user_model, on_delete=models.CASCADE)
    property_license = models.CharField(max_length=128)
    profile_photo = models.ImageField(blank=True, default='default.jpg')

    def __str__(self):
        return self.user.email

    def get_fullname(self):
        return self.user.get_full_name()
