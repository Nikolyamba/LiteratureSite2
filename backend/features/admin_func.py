from backend.models import User
from backend.models.user import UserRole


def can_delete_user(current_user: User, target_user: User) -> bool:
    if current_user.role == UserRole.admin:
        return True
    if current_user == target_user:
        return True
    return False