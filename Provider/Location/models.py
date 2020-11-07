from django.db import models


# Create your models here.
class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField(max_length=256, verbose_name='Property Address')

    def __str__(self):
        return self.address
