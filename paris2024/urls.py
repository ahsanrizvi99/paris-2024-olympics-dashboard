from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('olympics.urls')),  # Includes URLs for the Olympics app
]
