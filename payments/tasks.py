from celery import shared_task

@shared_task(bind=True)
def send_notification(self, payer_username, payee_username, amount):
    message = f"{payer_username} enviou um pagamento para {payee_username} no valor de R$ {amount}"
    print(message)
    return {
        'status': 'success',
        'message': message
    }
