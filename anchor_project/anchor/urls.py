import polaris.urls
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(polaris.urls)),
    path('sep31/', include('anchor.sep31.urls')),
]
