from ninja import ModelSchema
from .models import Transaction

class TransactionSchema(ModelSchema):
    class Meta:
        model = Transaction
        exclude = ['id', 'date']
        
    