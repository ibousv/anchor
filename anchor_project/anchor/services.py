#SEP12 ()
# services.py

def fields_for_type(client_type):
    """
    Retourne les champs KYC requis pour le type de client donné.
    
    :param client_type: 'individual' ou 'corporate'
    :return: Un dictionnaire avec les champs KYC requis.
    """
    if client_type == 'individual':
        return {
            'first_name': 'Le prénom du client',
            'last_name': 'Le nom du client',
            'email': 'L’adresse email du client',
            'phone_number': 'Le numéro de téléphone du client',
            'photo_id_front': 'Photo d’identité (avant)',
            'photo_id_back': 'Photo d’identité (arrière)',
        }
    elif client_type == 'corporate':
        return {
            'company_name': 'Nom de l’entreprise',
            'registration_number': 'Numéro d’enregistrement de l’entreprise',
            'email': 'Adresse email de l’entreprise',
            'phone_number': 'Numéro de téléphone de l’entreprise',
        }
    else:
        raise ValueError("Type de client non valide. Utilisez 'individual' ou 'corporate'.")
