from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Product, Sale, SaleItem

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
    ('Qo\'shimcha ma\'lumotlar', {'fields': ('role',)}),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock_quantity', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('name',)

    list_select_related = ('category',)

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'unit_price')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'cashier', 'total_amount', 'created_at']
    list_filter = ('created_at', 'cashier')

    list_select_related = ('cashier',)

    inlines = [SaleItemInline]
