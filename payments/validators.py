from decimal import Decimal
from django.core.exceptions import ValidationError

def validate_amount(value: Decimal):
    if value <= 0:
        raise ValidationError('Valor deve ser maior que zero')
    if value > Decimal('100000'):
        raise ValidationError('Valor máximo permitido é R$ 100.000,00')
