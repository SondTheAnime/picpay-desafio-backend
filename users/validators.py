from django.core.exceptions import ValidationError

def validate_cpf(value):
    # Remove caracteres especiais
    value = value.replace('.', '').replace('-', '').replace(' ', '')

    # Validações básicas
    if not value:
        raise ValidationError('CPF é obrigatório')
    
    if not value.isdigit():
        raise ValidationError('CPF deve conter apenas números')
    
    if len(value) != 11:
        raise ValidationError('CPF deve ter 11 dígitos')

    # Verifica se todos os dígitos são iguais
    if len(set(value)) == 1:
        raise ValidationError('CPF inválido - todos os dígitos são iguais')

    # Validação do primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(value[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    if int(value[9]) != digito1:
        raise ValidationError('CPF inválido - primeiro dígito verificador incorreto')

    # Validação do segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(value[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    if int(value[10]) != digito2:
        raise ValidationError('CPF inválido - segundo dígito verificador incorreto')

    # Verifica se é um CPF conhecido inválido
    cpfs_invalidos = [
        '00000000000',
        '11111111111',
        '22222222222',
        '33333333333',
        '44444444444',
        '55555555555',
        '66666666666',
        '77777777777',
        '88888888888',
        '99999999999'
    ]
    
    if value in cpfs_invalidos:
        raise ValidationError('CPF inválido')
