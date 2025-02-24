# services.py
from django.core.exceptions import ValidationError
from .models import PolarisUser

class UserService:
    #SEP 12
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
        
    #SEP 24
    def user_for_account(self, account_id):
        """
        Récupère l'utilisateur associé à un identifiant de compte SEP-24.

        :param account_id: Identifiant unique du compte SEP-24.
        :return: L'utilisateur associé ou None si aucun utilisateur n'est trouvé.
        """
        try:
            user = PolarisUser.objects.get(account_id=account_id)
            return user
        except PolarisUser.DoesNotExist:
            return None
        
    #SEP 6
    def user_for_account(self, account_id):
        """
        Retourne l'utilisateur associé à un identifiant de compte donné.
        
        :param account_id: L'identifiant unique du compte.
        :return: L'utilisateur associé au compte.
        """
        try:
            # Rechercher l'utilisateur basé sur l'identifiant du compte
            user = PolarisUser.objects.get(account_id=account_id)
            return user
        except PolarisUser.DoesNotExist:
            raise ValidationError(f"Aucun utilisateur trouvé pour l'identifiant de compte : {account_id}")
        
    #SEP 31
    def user_for_id(self, user_id):
        """
        Retourne l'utilisateur associé à un identifiant utilisateur donné.
        
        :param user_id: L'identifiant unique de l'utilisateur.
        :return: L'utilisateur associé à cet identifiant.
        """
        try:
            # Rechercher l'utilisateur basé sur l'identifiant utilisateur
            user = PolarisUser.objects.get(id=user_id)
            return user
        except PolarisUser.DoesNotExist:
            raise ValidationError(f"Aucun utilisateur trouvé pour l'identifiant utilisateur : {user_id}")      
    def verify_bank_account(self, account_number, bank_code):
        """
        Vérifie la validité d'un compte bancaire donné en se basant sur les standards de SEP-31.
    
        :param account_number: Le numéro de compte bancaire à vérifier.
        :param bank_code: Le code de la banque associé au compte.
        :return: True si le compte est valide, False sinon.
        """
        # Logique de vérification du compte bancaire basée sur SEP-31
        # on peut  ajouter ici une requête à une API de validation bancaire ou une logique propre.
    
        if account_number and bank_code:
          # Simulation  d'une vérification simple (à remplacer par une logique SEP-31 réelle)
          if len(account_number) == 10 and len(bank_code) == 5:
            return True
          else:
            raise ValidationError("Le numéro de compte bancaire ou le code de la banque est invalide.")
        else:
           raise ValidationError("Le numéro de compte bancaire ou le code de la banque est manquant.")
          
