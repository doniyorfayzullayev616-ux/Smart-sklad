from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Categories, Product, Sale
from .serializers import CategorySerializer, ProductSerializer, SaleSerializer
from django.shortcuts import render
from rest_framework import filters
import csv
from django.http import HttpResponse
from .models import Product

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

