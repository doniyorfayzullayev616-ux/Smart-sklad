from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import SaleItem, Product

@receiver(post_delete, sender=SaleItem)
def restore_product_stock(sender, instance, **kwargs):
    """
    Chek yoki uning ichidagi tovar o'chirilganda sotilgan tovarlar
    sonini ombor qoldig'iga avtomat qaytaradi.
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """

    with transaction.atomic():

        product = Product.objects.select_for_update().get(id=instance.product.id)

        product.stock_quantity += instance.quantity
        product.save()

        print(f"SIRENA: {product.name} dan {instance.quantity} ta omborga qaytarildi.")