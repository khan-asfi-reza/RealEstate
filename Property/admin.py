from django.contrib import admin

# Register your models here.
from Property.models import Property, Property_Images, Property_Video

admin.site.register(Property)
admin.site.register(Property_Images)

admin.site.register(Property_Video)
