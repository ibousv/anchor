from django.http import JsonResponse
from django.http import JsonResponse, Http404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SEP38Conversion

def get_prices(request):
    source_asset = request.GET.get('source_asset')  # Actif source (ex: USD)
    destination_asset = request.GET.get('destination_asset')  # Actif de destination (ex: EUR)

    # Exemple de taux de conversion (à remplacer par votre logique métier)
    rate = 0.85  # 1 USD = 0.85 EUR

    return JsonResponse({
        'source_asset': source_asset,
        'destination_asset': destination_asset,
        'rate': str(rate)
    })


@csrf_exempt
def create_conversion(request):
    if request.method == 'POST':
        data = request.POST  # Ou request.json si vous utilisez JSON
        conversion = SEP38Conversion.objects.create(
            conversion_id=data['conversion_id'],
            source_asset=data['source_asset'],
            destination_asset=data['destination_asset'],
            rate=data['rate'],
            status="pending"
        )
        return JsonResponse({
            'id': conversion.conversion_id,
            'status': conversion.status
        })
    return JsonResponse({'error': 'Invalid request method'}, status=400)



def get_conversion(request, conversion_id):
    try:
        conversion = SEP38Conversion.objects.get(conversion_id=conversion_id)
        return JsonResponse({
            'id': conversion.conversion_id,
            'status': conversion.status,
            'source_asset': conversion.source_asset,
            'destination_asset': conversion.destination_asset,
            'rate': str(conversion.rate)
        })
    except SEP38Conversion.DoesNotExist:
        raise Http404("Conversion not found")