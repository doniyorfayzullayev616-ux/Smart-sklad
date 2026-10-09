from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

#1. Custom User - Rollarni boshqarish uchun
class User(AbstractUser):
    ROLE_CHOICES = (
    ('ADMIN', 'Admin'),
    ('CASHIER', 'Cashier'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CASHIER')

    def __str__(self):
        return f"{self.username} ({self.role}"

# Barcha modellar uchun umumiy vaqt maydonlari (DRY tamoyili)
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True

# Ombor bo'limi
class Categories(BaseModel):
    name = models.CharField(max_length=100, unique = True)

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, related_name='products')
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])
    stock_quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])  #Ombor qoldig'i minusga kirmasligi shart.

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']

# Savdo (kassa) bo'limi
class Sale(BaseModel):
    cashier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sales')
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Chek #{self.id} - {self.total_amount} UZS"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT) # SOTILGAN TOVArni bazadan o'chirib bo'lmaydi
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2) # sotilgan paytidagi narx(tarix uchun)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"