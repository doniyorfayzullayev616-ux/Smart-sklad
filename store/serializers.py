from rest_framework import serializers
from .models import Categories, Product, Sale, SaleItem

from django.db import transaction
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'unit_price']
        # unit_price frontenddan kelmaydi, uni o'zimiz backendda beramiz
        read_only_fields = ['unit_price']

class SaleSerializer(serializers.ModelSerializer): # Ichma ich serializer: bitta chek ichida bir necha tovarlar ro'yxati
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'cashier', 'total_amount', 'created_at', 'items']
        #kassir, umumiy summa va vaqtni o'zimiz avtomat to'ldiramiz
        read_only_fields = ['cashier', 'total_amount', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        # so'rov yuborayotgan foydalanuvchini JWT tokendan olamiz
        user = self.context['request'].user

        #tranzaksiyani boshlash
        with transaction.atomic(): #avval bosh chek sale yaratamiz
            sale = Sale.objects.create(cashier=user, total_amount=0, **validated_data)
            total_amount = Decimal('0.00')

            for item_data in items_data:
                product = Product.objects.select_for_update().get(id=item_data['product'].id)
                quantity = item_data['quantity']

                # 1-qadam: Ombor qoldigini tekshirish (validation)
                if product.stock_quantity < quantity:
                    raise serializers.ValidationError(
                        f"Xatolik: {product.name} mahsulotidan omborda yetarli emas! Qoldiq: {product.stock_quantity} dona."

                    )
                #2-qadam: Ombor qoldigini kamaytirish
                product.stock_quantity -= quantity
                product.save()

                #3-qadam: Narxni bazadan olib, SaleItem yaratish
                unit_price = product.price
                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price
                )

                #4-qadam: chekning umumiy summasini hisoblab borish
                total_amount += (unit_price * quantity)

            #sikl tugagach, hisoblangan umumiy summani chekga yozib saqlaymiz
            sale.total_amount = total_amount
            sale.save()

            return sale

