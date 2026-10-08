from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, SaleViewSet
from .views import login_page, dashboard_page


# Router yaratamiz va viewlarimizni unga ro'yxatdan o'tkazamiz
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'sales', SaleViewSet) # Savdo API si qo'shildi

urlpatterns = [
    path('', include(router.urls)),
    path('login-ui/', login_page, name='login_ui'),
    path('dashboard/', dashboard_page, name='dashboard'),
]

