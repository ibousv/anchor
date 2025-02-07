from django.db import models

class SEP31Transaction(models.Model):
    transaction_id = models.CharField(max_length=255, unique=True)  # ID unique de la transaction
    sender_id = models.CharField(max_length=255)  # ID de l'expéditeur
    receiver_id = models.CharField(max_length=255)  # ID du destinataire
    amount = models.DecimalField(max_digits=20, decimal_places=7)  # Montant de la transaction
    asset = models.CharField(max_length=255)  # Actif Stellar (ex: USD)
    status = models.CharField(max_length=50, default="pending")  # Statut de la transaction
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création
    updated_at = models.DateTimeField(auto_now=True)  # Date de mise à jour

    def __str__(self):
        return self.transaction_id