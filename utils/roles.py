# utils/roles.py

def get_user_role(user):
    """Повертає назву першої ролі користувача або None."""
    if user.is_authenticated:
        groups = user.groups.all()
        if groups.exists():
            return groups[0].name
    return None


def has_role(user, *roles):
    """Перевіряє, чи має користувач хоча б одну з переданих ролей."""
    user_role = get_user_role(user)
    return user_role in roles


def get_role_permissions():
    """
    Словник: роль → доступні дії
    Додаєш нову роль — додаєш сюди
    """
    return {
        'Курсант': ['view_self'],
        'Журналіст': ['view_self', 'view_group', 'edit_grades'],
        'Командир': ['view_self', 'view_group', 'edit_grades', 'edit_duties'],
        'Начальник курсу': ['view_all'],
        'Адмін': ['full_access'],
    }


def user_can(user, permission):
    """Перевіряє, чи користувач має дозвіл на дію"""
    role = get_user_role(user)
    permissions = get_role_permissions().get(role, [])
    return permission in permissions or 'full_access' in permissions
