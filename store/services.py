import os
from django.utils import timezone
from django.db.models import Sum, F
from google import genai
from .models import Product, SaleItem

def generate_daily_ai_report():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return "Gemini API kaliti topilmadi"

    client = genai.Client(api_key=api_key)

    today = timezone.now().date()

    # 1. Bugungi umumiy savdolar va tushum
    today_sales = SaleItem.objects.filter(sale__created_at__date=today)


    total_revenue = today_sales.aggregate(
        total=Sum(F('unit_price') * F('quantity')))['total'] or 0

    total_items_sold = today_sales.aggregate(
        total=Sum('quantity')
    )['total'] or 0


    # 2. Qoldig'i 5 tadan kam qolgan tovarlar
    low_stock_products = Product.objects.filter(stock_quantity__lt=5, is_active=True).values_list('name', 'stock_quantity')
    low_stock_list = [f"{name} ({qty} dona)" for name, qty in low_stock_products]

    # 3. Gemini uchun ixcham ma'lumotlar matni
    summary_context = f"""
    Sana: {today}
    Kunning umumiy tushumi: {total_revenue} so'm
    Sotilgan umumiy tovarlar miqdori: {total_items_sold} ta
    O'rtacha bitta tovar narxi (o'rtacha chek): {average_price} so'm
    Omborda tugab borayotgan tovarlar: {', '.join(dead_stock_list) if dead_stock_list else "Barcha tovarlar yetarli"}
    Omborda chang bosib yotgan (zaxiralar katta) tovarlar: {', '.join(dead_stock_list) if dead_stock_list else "Yo'q"}
    """

    prompt = f"""
    Sen 30 yillik savdo tajribasiga ega, o'zbek bozorini ipidan ignasigacha biladigan aqlli biznes-maslahatchisan.
    Do'kon egasiga raqamlarni qaytarmasdan, faqatgina daromadni oshirish uchun 3 ta qat'iy, amaliy ko'rsatma ber:

    1. JAVONLAR ARXITEKTURASI: Tugayotgan (xodovoy) tovarlarga qarab, xaridorlar yana nima izlashi mumkinligini tahlil qil. Xodovoy tovarlarning yoniga do'kondagi qaysi mahsulotlarni yonma-yon qo'yish kerakligi haqida aniq maslahat ber.
    
    2. MUZLAGAN KAPITALNI QUTQARISH: Omborda zaxirasi katta bo'lib qotib qolgan ({', '.join(dead_stock_list) if dead_stock_list else 'yo\'q'}) tovarlarni tezroq pulga aylantirish uchun nima qilish kerak? (Masalan: Xodovoy tovar bilan qo'shib sotish, kassa yoniga qo'yish). Bitta tayyor strategiya ber.
    
    3. TA'MINOT VA KASSIR NAZORATI: Tugayotgan tovarlar bo'yicha qaysi postavshikka zakaz berishni tayinla va bugungi o'rtacha xarid summasidan ({average_price} so'm) kelib chiqib, ertaga kassir mijozlarga nimalarni faol taklif qilishi kerakligini uqtir.
    
    Matn qisqa, londa va haqiqiy tadbirkorlar tilida bo'lsin.
    """

    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        logger.error(f"Gemini API xatoligi: {str(e)}")
        return f"Tizim xabari: Kunlik savdo ma'lumotlari saqlandi. (Tarmoq uzilishi sababli AI biznes-tahlili vaqtincha ishlamayapdi."