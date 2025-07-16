from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('select2/', include('django_select2.urls')),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('profile/', include('profiles.urls'))
]
