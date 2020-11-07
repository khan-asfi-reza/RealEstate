
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from RentDay import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('Accounts.urls')),
                  path('api/location/', include('Provider.Location.urls')),
                  path('api/property/', include('Property.urls'))



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
