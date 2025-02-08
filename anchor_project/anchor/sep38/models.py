from django.db import models

class SEP38Conversion(models.Model):
    conversion_id = models.CharField(max_length=255, unique=True)  # ID unique de la conversion
    source_asset = models.CharField(max_length=255)  # Actif source (ex: USD)
    destination_asset = models.CharField(max_length=255)  # Actif de destination (ex: EUR)
    rate = models.DecimalField(max_digits=20, decimal_places=7)  # Taux de conversion
    status = models.CharField(max_length=50, default="pending")  # Statut de la conversion
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création
    updated_at = models.DateTimeField(auto_now=True)  # Date de mise à jour

    def __str__(self):
        return self.conversion_id