from stellar_sdk import Keypair
from anchor.models import Asset
import django
django.setup()

def generate_stellar_keys():
    """ Génère une paire de clés pour l'émetteur et le distributeur """
    issuer = Keypair.random()
    distributor = Keypair.random()

    # Stocker les clés secrètes en local
    with open("secretKeys.txt", "w") as f:
        f.write(f"Issuer Secret: {issuer.secret}\n")
        f.write(f"Distributor Secret: {distributor.secret}\n")

    return {
        "issuer_public": issuer.public_key,
        "issuer_secret": issuer.secret,
        "distributor_public": distributor.public_key,
        "distributor_secret": distributor.secret
    }
    
def create_stellar_assets(asset_list=None):
    """ Crée plusieurs actifs Stellar et les enregistre dans Polaris """
    if asset_list is None:
        asset_list = [
            {"code": "TEST", "symbol": "$"},
            {"code": "USDC", "symbol": "$"},
        ]

    assets = []
    
    for asset_data in asset_list:
        keys = generate_stellar_keys()

        asset = Asset.objects.create(
            code=asset_data["code"],
            issuer=keys["issuer_public"],
            distribution_seed=keys["distributor_secret"],  # Clé cryptée en DB
            sep24_enabled=True,
            sep6_enabled=True,
            deposit_enabled=True,
            withdrawal_enabled=True,
            symbol=asset_data["symbol"]
        )

        assets.append(asset)
        print(f"Actif {asset_data['code']} créé avec succès !")
    
    return assets

