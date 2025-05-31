# accounts/context_processors.py
from utils.roles import get_user_role

def user_role(request):
    return {'role': get_user_role(request.user)}
