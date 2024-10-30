from django.db import models
from decimal import Decimal
from users.models import User
from django_celery_results.models import TaskResult

# Create your models here.
class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), editable=False)
    payer = models.ForeignKey(User, on_delete=models.DO_NOTHING, editable=False)
    payee = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='payee_user', editable=False)
    date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.payer} -> {self.payee} - {self.amount}'

class CeleryTask(TaskResult):
    class Meta:
        proxy = True
        verbose_name = 'Tarefa Celery'
        verbose_name_plural = 'Tarefas Celery'


