import os
from django.utils import timezone
from django.db.models import Sum, F
import google.generativeai as genai
from .models import Product, SaleItem
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class AiReportThrottle(UserRateThrottle):
    scope = 'ai_report'

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@throttle_classes([AiReportThrottle])
def get_ai_daily_report(request):
    if not(request.user.is_staff or request.user.is_superuser):
        return Response({"error": "Faqat rahbar uchun ruxsat berilgan"}, status = 403)
    report_text = generate_daily_ai_report()
    return Response({'report': report_text})

api_key = os.getenv('GEMINI_API_KEY')
if api_key:
    genai.configure(api_key=api_key)


def generate_daily_ai_report():
    today = timezone.now().date()

    # 1. Bugungi umumiy savdolar va tushum
    today_sales = SaleItem.objects.filter(sale__created_at__date=today)


    total_revenue = today_sales.aggregate(
        total=Sum(F('unit_price') * F('quantity')))['total'] or 0

    total_items_sold = today_sales.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    top_selling = today_sales.values('product__name').annotate(
        total_qty=Sum('quantity')
    ).order_by('-total_qty')[:3]

    top_selling_list = [f"{item['product__name']} ({item['total_qty']} ta)" for item in top_selling]


    # 2. Qoldig'i 5 tadan kam qolgan tovarlar
    low_stock_products = Product.objects.filter(stock_quantity__lt=5).values_list('name', 'stock_quantity')
    low_stock_list = [f"{name} ({qty} dona)" for name, qty in low_stock_products]

    # 3. Gemini uchun ixcham ma'lumotlar matni
    summary_context = f"""
    Bugungi sana: {today}
    Bugungi jami tushum: {total_revenue} so'm
    Sotilgan umumiy tovarlar miqdori: {total_items_sold} ta
    Bugungi eng xaridorgir tovarlar (Top-3): {', '.join(top_selling_list) if top_selling_list else "Hozircha savdo yo'q"}
    Omborda tugab borayotgan tovarlar: {', '.join(low_stock_list) if low_stock_list else "Barcha tovarlar zaxirasi yetarli darajada"}
    """

    prompt = f"""
    Sen Smart-Sklad tizimining tajribali moliyaviy analitikisan.
    Do'kon rahbariga quyidagi statistikaga asoslanib, quruq gaplarsiz, to'g'ridan-to'g'ri 3 ta qismdan iborat strategik hisobot tayyorlab ber.
    Javobing faqat O'zbek tilida bo'lsin va qat'iy ravishda quyidagi tuzilmaga amal qilsin:

    Ma'lumotlar:
    {summary_context}
    
    Talab qilinadigan format (xuddi shunday emojilar va sarlavhalar bilan yoz):
    1. 📊 Moliyaviy Holat: (Bugungi tushum va savdoni tortib ketgan asosiy tovarlar haqida 1-2 jumla).
    2. ⚠️ Zaxira Xavfi: (Tugayotgan tovarlar bo'yicha zudlik bilan nima qilinishi kerakligi).
    3. 💡 Strategik Maslahat: (Ertangi kun tushumini oshirish uchun aniq 1 ta biznes taklif).
    """

    try:
        model = genai.GenerativeModel('gemini-3.8-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Hisobot shakllantirishda xatolik: {str(e)}"