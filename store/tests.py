from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Categories, Product, Sale, SaleItem

class SaleTransaction(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.kassir = User.objects.create_user(username="test_kassir", password="123")

        self.kategoriya = Categories.objects.create(name="Elektronika")

        self.mahsulot = Product.objects.create(
            name="Test Noutbuk",
            category=self.kategoriya,
            stock_quantity=10,
            price=1500,
            is_active = True
        )

        self.savdo_cheki = Sale.objects.create(
            cashier=self.kassir,
            total_amount=4500
        )

        self.savdo_qatori = SaleItem.objects.create(
            sale=self.savdo_cheki,
            product=self.mahsulot,
            quantity=3,
            unit_price=1500
        )

        self.mahsulot.stock_quantity = 7
        self.mahsulot.save()

    def test_delete_sale_restores_stock(self):


        self.client.force_authenticate(user=self.kassir)

        url = f"/api/sales/{self.savdo_cheki.id}/"
        response = self.client.delete(url)

        self.mahsulot.refresh_from_db()

        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.mahsulot.stock_quantity, 10)


    def test_create_sale_insufficient_stock(self):

        self.client.force_authenticate(user=self.kassir)

        payload = {
            "items": [
                {
                    "product": self.mahsulot.id,
                    "quantity": 15,
                }
            ]
        }

        url = "/api/sales/"
        response = self.client.post(url, data=payload, format="json")

        self.mahsulot.refresh_from_db()
        self.assertEqual(self.mahsulot.stock_quantity, 7)


    def test_create_sale_success(self):
        self.client.force_authenticate(user=self.kassir)

        payload = {
            "items": [
                {
                    "product": self.mahsulot.id,
                    "quantity": 2
                }
            ]
        }

        url = "/api/sales/"
        response = self.client.post(url, data=payload, format="json")

        print(f"\n-- {response.data}")
        if response.status_code != 201:
            print(f"xatolik : {response.data}")

        self.assertEqual(response.status_code, 201)

        self.mahsulot.refresh_from_db()
        self.assertEqual(self.mahsulot.stock_quantity, 5)

    def test_create_sale_negative_quantity(self):
        self.client.force_authenticate(user=self.kassir)

        payload = {
            "items": [
                {
                    "product": self.mahsulot.id,
                    "quantity": -5
                }
            ]
        }

        url = "/api/sales/"
        response=self.client.post(url, data=payload, format="json")

        print(f"\n haker tizim javobi:{response.status_code}")
        if response.status_code == 201:
            print("tizim buzildi!")

        self.assertEqual(response.status_code, 400)

        self.assertEqual(self.mahsulot.stock_quantity, 7)

    def test_anonymous_export_blocked(self):
        """1-hujum: Anonim eksportni yuklab olmoqchi"""

        self.client.force_authenticate(user=None)

        url = "/api/export/excel/"
        response = self.client.get(url)

        print(f"\n-- anonim javobi: {response.status_code}")

        self.assertEqual(response.status_code, 401)

    def test_cashier_cannot_change_price(self):
        """2-hujum: Kassir tovar narxini o'zgartirmoqchi aldamchilik qilib"""

        self.client.force_authenticate(user=self.kassir)

        url = f"/api/products/{self.mahsulot.id}/"
        payload = {"price": 100}

        response = self.client.patch(url, data=payload, format="json")

        print(f"\n-- Kassir narx o'zgartirganda javob: {response.status_code}--")

        self.assertEqual(response.status_code, 403)

        self.mahsulot.refresh_from_db()
        self.assertNotEqual(self.mahsulot.price, 100)