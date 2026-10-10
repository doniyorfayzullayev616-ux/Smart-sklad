from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet, SaleViewSet,
    login_page, dashboard_page, check_user_role, get_ai_daily_report
)


# Router yaratamiz va viewlarimizni unga ro'yxatdan o'tkazamiz
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'sales', SaleViewSet) # Savdo API si qo'shildi

urlpatterns = [
    path('', include(router.urls)),
    path('login-ui/', login_page, name='login_ui'),
    path('dashboard/', dashboard_page, name='dashboard'),

    path('user-role/', check_user_role, name='user-role'),
    path('ai-report/', get_ai_daily_report, name='ai-report'),
]

