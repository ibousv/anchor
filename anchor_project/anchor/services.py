# services.py
from django.core.exceptions import ValidationError
from .models import PolarisUser

class UserService:
    def create_user(self, first_name, last_name, email, phone_number=None, photo_id_front=None, photo_id_back=None):
        """
        Crée un utilisateur après avoir vérifié que l'email est unique.
        
        :param first_name: Prénom de l'utilisateur.
        :param last_name: Nom de l'utilisateur.
        :param email: Email de l'utilisateur.
        :param phone_number: Numéro de téléphone (facultatif).
        :param photo_id_front: Photo d'identité avant (facultatif).
        :param photo_id_back: Photo d'identité arrière (facultatif).
        :return: L'utilisateur créé.
        """
        # Vérification que l'email est unique
        if PolarisUser.objects.filter(email=email).exists():
            raise ValidationError("L'email est déjà utilisé.")
        
        # Création de l'utilisateur
        user = PolarisUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            photo_id_front=photo_id_front,
            photo_id_back=photo_id_back
        )
        
        return user

    def fields_for_type(self, user_type):
        """
        Retourne les champs KYC requis en fonction du type d'utilisateur (individual ou corporate).
        
        :param user_type: 'individual' ou 'corporate'.
        :return: Un dictionnaire contenant les champs nécessaires.
        """
        if user_type == 'individual':
            return {
                'first_name': 'Le prénom du client',
                'last_name': 'Le nom du client',
                'email': 'L’adresse email du client',
                'phone_number': 'Le numéro de téléphone du client',
                'photo_id_front': 'Photo d’identité (avant)',
                'photo_id_back': 'Photo d’identité (arrière)',
            }
        elif user_type == 'corporate':
            return {
                'company_name': 'Nom de l’entreprise',
                'registration_number': 'Numéro d’enregistrement de l’entreprise',
                'email': 'Adresse email de l’entreprise',
                'phone_number': 'Numéro de téléphone de l’entreprise',
            }
        else:
            raise ValueError("Type d'utilisateur non reconnu. Utilisez 'individual' ou 'corporate'.")
