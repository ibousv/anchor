from django.urls import path
from .views import create_transaction, get_transaction, update_transaction

urlpatterns = [
    path('transactions/', create_transaction, name='create_transaction'),
    path('transactions/<str:transaction_id>/', get_transaction, name='get_transaction'),
    path('transactions/<str:transaction_id>/', update_transaction, name='update_transaction'),
]