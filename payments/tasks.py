from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 3},
    soft_time_limit=30
)
def send_notification(self, payer_username, payee_username, amount):
    try:
        message = f"{payer_username} enviou um pagamento para {payee_username} no valor de R$ {amount}"
        logger.info(f"Enviando notificação: {message}")
        return {
            'status': 'success',
            'message': message
        }
    except Exception as e:
        logger.error(f"Erro ao enviar notificação: {str(e)}")
        raise self.retry(exc=e)
