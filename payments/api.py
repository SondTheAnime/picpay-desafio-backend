import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from ninja import Router
from .schemas import TransactionSchema
from users.models import User
from .models import Transaction
from django.shortcuts import get_object_or_404
from rolepermissions.checkers import has_permission
from django.db import transaction as django_transaction
from core.settings import AUTHORIZE_TRANSFER_ENDPOINT
from .tasks import send_notification


payments_router = Router()

def authorize_transaction():
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504]
    )
    
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = session.get(
            AUTHORIZE_TRANSFER_ENDPOINT,
            headers=headers,
            timeout=5
        )
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        response_data = response.json()
        print(f"Parsed response: {response_data}")
        
        if response_data.get('status') == 'success' and response_data.get('data', {}).get('authorization'):
            return {"status": 200, "message": "Transação autorizada"}
        else:
            return {"status": 400, "message": "Transação não autorizada"}
        
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {str(e)}")
        return {"status": 400, "message": "Serviço de autorização indisponível"}
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        return {"status": 400, "message": "Erro ao processar autorização"}
    finally:
        session.close()

@payments_router.post('/', response={200: dict, 400: dict, 403: dict})
def transaction(request, transaction_data: TransactionSchema):
    try:
        payer = get_object_or_404(User, id=transaction_data.payer)
        payee = get_object_or_404(User, id=transaction_data.payee)
        
        if payer.amount < transaction_data.amount:
            return 400, {'error': 'Saldo insuficiente'}
        
        if not has_permission(payer, 'make_transfer'):
            return 403, {'error': 'Você não tem permissão para realizar transferências'}
        
        if not has_permission(payee, 'receive_transfer'):
            return 403, {'error': 'O usuário não tem permissão para receber transferências'}
        
        with django_transaction.atomic():
            payer.pay(transaction_data.amount)
            payee.receive(transaction_data.amount)
            
            transct = Transaction(
                amount=transaction_data.amount,
                payer_id=transaction_data.payer,
                payee_id=transaction_data.payee
            )
            payer.save()
            payee.save()
            transct.save()
            
            auth_response = authorize_transaction()
            if auth_response.get('status') == 200:
                # Mesmo que a notificação falhe, a transação é considerada um sucesso
                send_notification.apply_async(args=[payer.username, payee.username, str(transaction_data.amount)])
                return 200, {'message': 'Transação realizada com sucesso'}
            else:
                django_transaction.set_rollback(True)
                return 400, {'error': auth_response.get('message', 'Transação não autorizada')}
                
    except Exception as e:
        return 400, {'error': str(e)}
    