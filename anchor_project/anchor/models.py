from django.db import models

class PolarisUser(models.Model):
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    photo_id_front = models.ImageField(upload_to='photos/front/', null=True, blank=True)  # Image réelle côté avant du PI
    photo_id_back = models.ImageField(upload_to='photos/back/', null=True, blank=True)  # Image réelle côté arrière du PI
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
