from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Categories, Product, Sale
from .serializers import CategorySerializer, ProductSerializer, SaleSerializer
from django.shortcuts import render
import csv
from django.http import HttpResponse
from .models import Product

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import generate_daily_ai_report

from rest_framework import filters

from rest_framework import status
from rest_framework.response import Response

class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs): # asl login jarayonini ishga tushiramiz
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data['access']

            #tokenni httponly cookie ga joylaymiz(XSS hujumidan 100% himoya)
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True, # JavaScript orqali o'qishni taqiqlaydi
                samesite='Lax', # boshqa saytlardan so'rov kelishini to'sadi
                max_age=3600*24 # 1 kunga yaroqli
            )
            # xavfsizlik uchun tokenni ochiq javobdan (JSON dan) o'chirib tashlaymiz
            del response.data['access']
            if 'refresh' in response.data:
                del response.data['refresh']

            response.data['message'] = "Tizimga muvaffaqiyatli kirdingiz!"

        return response

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action in ['retrieve', 'update', 'partial_update','destroy']:
            return queryset

        is_archived = self.request.query_params.get('archived')
        if is_archived == 'true':
            queryset = queryset.filter(is_active=False)
        else:
            queryset = queryset.filter(is_active=True)

        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id = category_id)

        return queryset


    def destroy(self, request, *args, **kwargs):
        instance=self.get_object()
        instance.is_active=False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]


def login_page(view):
    return render(view, 'login.html')

def dashboard_page(request):
    return render(request, 'dashboard.html')

def export_products_excel(request):      #brauzerga bu oddiy sahifa emas, balki yuklab olinadigan fayl ekanligini aytamiz
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Sklad_Hisobot.csv"'

    writer=csv.writer(response)

    writer.writerow(['ID', 'Mahsulot Nomi', 'Kategoriya ID', 'Narxi(so\'m', 'Qoldiq (dona)'])

    products = Product.objects.all().values_list('id', 'name', 'category_id', 'price', 'stock_quantity')
    for product in products:
        writer.writerow(product)

    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_user_role(request):  # Foydalanuvchi admin (staff yoki superuser) ekanligini tekshiramiz
    is_admin = request.user.is_staff or request.user.is_superuser
    return Response({"is_admin": is_admin})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ai_daily_report(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return Response({"error": "Faqat rahbar uchun ruxsat berilgan"}, status=403)

    report_text = generate_daily_ai_report()
    return Response({"report": report_text})

