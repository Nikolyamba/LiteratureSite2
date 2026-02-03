import uuid

from backend.models import User
from backend.models.user import UserRole

def can_edit_user(current_user: User, target_user: User) -> bool:
    if current_user.role == UserRole.admin:
        return True
    if current_user == target_user:
        return True
    return False

def can_edit_comment(current_user: User, user_id: uuid.UUID) -> bool:
    if current_user.role == UserRole.admin:
        return True
    if current_user.id == user_id:
        return True
    return False

def isAdmin(current_user: User) -> bool:
    if current_user.role == UserRole.admin:
        return True
    return False