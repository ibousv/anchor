from django.urls import path
from .views import get_prices, create_conversion, get_conversion

urlpatterns = [
    path('prices/', get_prices, name='get_prices'),
    path('conversions/', create_conversion, name='create_conversion'),
    path('conversions/<str:conversion_id>/', get_conversion, name='get_conversion'),
]