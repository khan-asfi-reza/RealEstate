from django.urls import path

from .views import LocationView

urlpatterns = [
    path('', LocationView.as_view(), name='location')
]
