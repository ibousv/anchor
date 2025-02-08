import polaris.urls
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(polaris.urls)),
    path('sep38/', include('anchor.sep38.urls'))
]
