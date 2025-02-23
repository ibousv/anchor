import pytest
from anchor  import create_stellar_assets
from anchor.models import Asset

@pytest.mark.django_db  # Permet d'utiliser la base de données de test
def test_create_stellar_assets():
    assets = create_stellar_assets([
        {"code": "TEST", "symbol": "$"},
        {"code": "USDC", "symbol": "$"}
    ])
    
    assert len(assets) == 2  # Vérifie que 2 actifs ont été créés
    assert Asset.objects.filter(code="USDC").exists()  # Vérifie que USDC est bien enregistré
    assert Asset.objects.filter(code="TEST").exists()  # Vérifie que TEST est bien enregistré
