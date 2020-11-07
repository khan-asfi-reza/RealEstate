# Generated by Django 3.0.7 on 2020-06-26 14:59

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('Location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('Location',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Location.Location')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=64)),
                ('last_name', models.CharField(blank=True, max_length=64)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('account_type',
                 models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Renter'), (2, 'Agent'), (3, 'Admin')])),
                ('verified', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Renter_Property_Pref_Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office_type', models.PositiveSmallIntegerField(choices=[(1, 'Office'), (2, 'Home')], default=1,
                                                                 verbose_name='Work From')),
                ('desibel_rating', models.DecimalField(decimal_places=6, max_digits=8)),
                ('custom_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                      related_name='renter_custom_location', to='Location.Location',
                                                      verbose_name='Custom Location 1')),
                ('custom_location_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                        related_name='renter_custom2_location2', to='Location.Location',
                                                        verbose_name='Custom Location 2')),
                ('office_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                      related_name='renter_office_location', to='Location.Location',
                                                      verbose_name='Office Location')),
                ('renter',
                 models.OneToOneField(limit_choices_to={'account_type': 1}, on_delete=django.db.models.deletion.CASCADE,
                                      to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Renter_Property_Pref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_type',
                 models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Apartment'), (2, 'House'), (3, 'Room')])),
                ('bathrooms', models.PositiveIntegerField(blank=True)),
                ('bedrooms', models.PositiveIntegerField(blank=True)),
                ('parking_spot', models.PositiveIntegerField(blank=True)),
                ('move_in', models.DateField(blank=True)),
                ('suburb', models.PositiveIntegerField(blank=True)),
                ('min_price', models.IntegerField(blank=True)),
                ('max_price', models.IntegerField(blank=True)),
                ('location',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Location.Location')),
                ('user',
                 models.OneToOneField(limit_choices_to={'account_type': 1}, on_delete=django.db.models.deletion.CASCADE,
                                      to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Renter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender',
                 models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female'), (3, 'Others')])),
                ('status', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Student'), (2, 'Worker'),
                                                                                 (3, 'Businessman')])),
                ('occupation', models.CharField(blank=True, max_length=64)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('income', models.PositiveIntegerField(blank=True)),
                ('income_pre_tax', models.PositiveIntegerField(blank=True)),
                ('people_living_with', models.PositiveSmallIntegerField(blank=True)),
                ('marital_status',
                 models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Married'), (2, 'Unmarried')])),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[
                    django.core.validators.RegexValidator(
                        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits Allowed",
                        regex='^\\+?1?\\d{9,15}$')])),
                ('profile_photo', models.ImageField(blank=True, default='default.jpg', upload_to='')),
                ('user',
                 models.OneToOneField(limit_choices_to={'account_type': 1}, on_delete=django.db.models.deletion.CASCADE,
                                      to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_license', models.CharField(max_length=128)),
                ('profile_photo', models.ImageField(blank=True, default='default.jpg', upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender',
                 models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female'), (3, 'Others')])),
                ('phone_number', models.CharField(max_length=14)),
                ('date_of_birth', models.DateField()),
                ('licence', models.CharField(max_length=128, verbose_name='RealState Licence')),
                ('profile_photo', models.ImageField(blank=True, default='default.jpg', upload_to='')),
                ('agency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                             related_name='agent_under_the_agency', to='Accounts.Agency')),
                ('suburbs', models.ManyToManyField(blank=True, to='Location.Location',
                                                   verbose_name='Suburbs Properties Available')),
                ('user',
                 models.ForeignKey(limit_choices_to={'account_type': 2}, on_delete=django.db.models.deletion.CASCADE,
                                   related_name='agent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('Accounts.user',),
        ),
    ]
