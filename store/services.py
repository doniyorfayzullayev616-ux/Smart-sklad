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
    low_stock_products = Product.objects.filter(stock_quantity__lt=5).values_list('name', 'stock_quantity')
    low_stock_list = [f"{name} ({qty} dona)" for name, qty in low_stock_products]

    # 3. Gemini uchun ixcham ma'lumotlar matni
    summary_context = f"""
    Bugungi sana: {today}
    Bugungi jami tushum: {total_revenue} so'm
    Sotilgan umumiy tovarlar miqdori: {total_items_sold} ta
    Omborda tugab borayotgan tovarlar: {', '.join(low_stock_list) if low_stock_list else "Barcha tovarlar yetarli"}
    """

    prompt = f"""
    Sen Smart-Sklad tizimining tajribali biznes tahlilchisisan.
    Quyidagi kunlik ma'lumotlar asosida do'kon egasiga qisqa (3-4 jumla), tushunarli va amaliy xulosa ber.
    Qaysi mahsulotga e'tibor qaratish kerakligini va do'kon holatini aniq ko'rsat. O'zbek tilida javob ber.

    Ma'lumotlar:
    {summary_context}
    """

    try:
        response = model.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Hisobot shakllantirishda xatolik: {str(e)}"