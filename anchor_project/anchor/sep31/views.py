from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SEP31Transaction
from django.http import JsonResponse, Http404

@csrf_exempt
def create_transaction(request):
    if request.method == 'POST':
        data = request.POST  # Ou request.json si vous utilisez JSON
        transaction = SEP31Transaction.objects.create(
            transaction_id=data['transaction_id'],
            sender_id=data['sender_id'],
            receiver_id=data['receiver_id'],
            amount=data['amount'],
            asset=data['asset'],
            status="pending"
        )
        return JsonResponse({
            'id': transaction.transaction_id,
            'status': transaction.status
        })
    return JsonResponse({'error': 'Invalid request method'}, status=400)



def get_transaction(request, transaction_id):
    try:
        transaction = SEP31Transaction.objects.get(transaction_id=transaction_id)
        return JsonResponse({
            'id': transaction.transaction_id,
            'status': transaction.status,
            'amount': str(transaction.amount),
            'asset': transaction.asset
        })
    except SEP31Transaction.DoesNotExist:
        raise Http404("Transaction not found")

from django.http import JsonResponse, Http404

@csrf_exempt
def update_transaction(request, transaction_id):
    if request.method == 'PATCH':
        try:
            transaction = SEP31Transaction.objects.get(transaction_id=transaction_id)
            data = request.POST  # Ou request.json si vous utilisez JSON
            if 'status' in data:
                transaction.status = data['status']
                transaction.save()
            return JsonResponse({
                'id': transaction.transaction_id,
                'status': transaction.status
            })
        except SEP31Transaction.DoesNotExist:
            raise Http404("Transaction not found")
    return JsonResponse({'error': 'Invalid request method'}, status=400)