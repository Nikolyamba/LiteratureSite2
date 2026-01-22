from backend.models import User
from backend.models.user import UserRole

def can_edit_user(current_user: User, target_user: User) -> bool:
    if current_user.role == UserRole.admin:
        return True
    if current_user == target_user:
        return True
    return False

def can_edit_book(current_user: User) -> bool:
    if current_user.role == UserRole.admin or current_user.role == UserRole.author:
        return True
    return False

def can_edit_genre(current_user: User) -> bool:
    return current_user.role == UserRole.admin