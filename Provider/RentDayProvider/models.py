from django.db import models


# Create your models here.
class Feature(models.Model):
    name = models.CharField(max_length=128, verbose_name='Features')
    description = models.CharField(max_length=512, verbose_name='Features Description')
    number = models.PositiveIntegerField(null=True)
