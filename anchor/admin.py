from django.contrib import admin
from .models import PolarisUser  # Import modèle PolarisUser

@admin.register(PolarisUser)
class PolarisUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number')  # Les colonnes affichées dans la liste des utilisateurs
    search_fields = ('first_name', 'last_name', 'email')  #  une barre de recherche pour ces champs
