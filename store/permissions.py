from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    faqat adminlarga (is_staff=True) yaratish, tahrirlash va o'chirish ruxsatini beradi.
    Kassirlar (yoki oddiy foydalanuvchilar) faqat ro'yxatni ko'ra oladi (GET so'rovi).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True


        return bool(request.user and request.user.is_authenticated and request.user.is_staff)