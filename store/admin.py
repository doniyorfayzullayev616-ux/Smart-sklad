from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Categories, Product, Sale, SaleItem

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
    ('Qo\'shimcha ma\'lumotlar', {'fields': ('role',)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(SaleItem)
