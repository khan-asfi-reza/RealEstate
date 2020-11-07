from django.urls import path

from .views import PropertyView, PropertyRetrieveUpdateDestroyView, ImageView, VideoView, ImageDetailView

urlpatterns = [

    path('', PropertyView.as_view(), name='property-view'),
    path('<pk>/', PropertyRetrieveUpdateDestroyView.as_view()),
    path('<pk>/images/', ImageView.as_view(), name='property-image-view'),
    path('<pk>/videos/', VideoView.as_view()),
    path('<prop>/images/<pk>/', ImageDetailView.as_view(), )
]
