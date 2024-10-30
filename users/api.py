from ninja import Router
from .schemas import TypeUserSchema
from .models import User
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .validators import validate_cpf
from rolepermissions.roles import assign_role

users_router = Router()

@users_router.post('/', response={201: dict, 400: dict, 500: dict})
def create_user(request, type_user_schema: TypeUserSchema):
    try:
        user_dict = type_user_schema.dict()
        print(user_dict)
        # Validar CPF antes de criar o usuário
        try:
            validate_cpf(user_dict['user']['cpf'])
        except ValidationError as e:
            return 400, {'error': str(e.messages[0])}
        
        user = User(**user_dict['user'])
        user.password = make_password(user.password)
        user.full_clean()
        user.save()
        assign_role(user, user_dict['type_user']['type'])
        
        return 201, {'message': 'Usuário criado com sucesso'}
    
    except IntegrityError as e:
        if 'username' in str(e):
            return 400, {'error': 'Username já está em uso'}
        elif 'email' in str(e):
            return 400, {'error': 'Email já está em uso'}
        elif 'cpf' in str(e):
            return 400, {'error': 'CPF já está em uso'}
        return 400, {'error': 'Erro ao criar usuário'}
    
    except ValidationError as e:
        errors = {}
        for field, messages in e.message_dict.items():
            errors[field] = messages[0]
        return 400, {'error': errors}
    
    except ValueError as e:
        return 400, {'error': str(e)}
    
    except Exception as e:
        print(e)
        return 500, {'error': 'Erro interno do servidor'}