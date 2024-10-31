from django.db import models
from decimal import Decimal
from users.models import User
from django_celery_results.models import TaskResult
from django.core.cache import cache

# Create your models here.
class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), editable=False)
    payer = models.ForeignKey(User, on_delete=models.DO_NOTHING, editable=False)
    payee = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='payee_user', editable=False)
    date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.payer} -> {self.payee} - {self.amount}'

    class Meta:
        indexes = [
            models.Index(fields=['payer', 'date']),
            models.Index(fields=['payee', 'date']),
        ]

    def save(self, *args, **kwargs):
        # Invalida o cache ao salvar
        cache_key = f'transaction_{self.id}'
        cache.delete(cache_key)
        super().save(*args, **kwargs)

class CeleryTask(TaskResult):
    class Meta:
        proxy = True
        verbose_name = 'Tarefa Celery'
        verbose_name_plural = 'Tarefas Celery'


