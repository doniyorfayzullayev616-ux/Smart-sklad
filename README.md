# 📦 Smart-Sklad - Ombor va Kassa Boshqaruv Tizimi

Smart-Sklad — bu do'kon va omborxonalar uchun mahsulotlarni, kassa jarayonlarini va ombor qoldiqlarini boshqarishga mo'ljallangan ishonchli, xavfsiz va to'liq avtomatlashtirilgan tizim. Loyiha zamonaviy biznes ehtiyojlarini hisobga olgan holda ishlab chiqilgan va Docker muhitiga qadoqlangan.

> ⚠️ **MUHIM OGOHLANTIRISH (ARXITEKTURA):**
> Ushbu loyihada kassa jarayonlarida (bir vaqtda sotishning oldini olish uchun) tranzaksiyalar xavfsizligi va qoldiqlar blokirovkasi (`select_for_update`) to'liq qo'llanilgan. Shu sababli, loyihani standart SQLite faylli bazasida **EMAS**, albatta Docker orqali (PostgreSQL bilan) ishga tushirish qat'iyan talab etiladi. SQLite bu blokirovkalarni to'g'ri o'qiy olmaydi.

## 🚀 Asosiy Imkoniyatlar (Features)

- **AI Kunlik Tahlilchi (Gemini 1.5 Flash):** Sun'iy intellekt orqali kunlik savdolar va ombor qoldiqlari bo'yicha "dead stock" va "low stock" kabi holatlarni hisobga oluvchi avtomatik biznes-tahlil.
- **Xavfsiz Avtorizatsiya (Cookie JWT):** XSS va CSRF hujumlaridan 100% himoyalangan (`Samesite=Strict`), JWT tokenlarni faqat `Secure` va `HttpOnly` cookie'larda saqlovchi zamonaviy xavfsizlik tizimi.
- **Brute-Force Himoyasi (Throttling):** API ga qilingan spam va xakerlik so'rovlarini avtomatik cheklovchi tizim (Anon va User rate limits).
- **Ma'lumotlar Butunligi (Soft Delete):** Mahsulotlarni o'chirmasdan "Arxivlash" va bekor qilingan cheklardagi tovarlarni omborga avtomatik qaytarish mantiqi.
- **Kassa va Tranzaksiyalar:** Xatoliklarni oldini olish uchun `transaction.atomic` yordamida ishonchli savdo amaliyotlari.
- **Hisobot (Export):** Ombor qoldiqlarini faqat vakolatli xodimlar uchun Excel (CSV) formatida eksport qilish.

## 🛠 Texnologiyalar (Tech Stack)

- *- **Backend:** Python 3.12, Django 5.x, Django REST Framework
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Ma'lumotlar bazasi:** PostgreSQL 15
- **Avtorizatsiya:** djangorestframework-simplejwt
- **Sun'iy Intellekt:** Google Gemini API
- **Infratuzilma:** Docker, Docker Compose

## ⚙️ Loyihani ishga tushirish (Local deployment)

Loyihani kompyuteringizda yurgizish uchun Docker va Docker Compose o'rnatilgan bo'lishi kerak. Boshqa hech qanday dastur yoki Python kutubxonasi talab etilmaydi.

1. Repozitoriyani kompyuterga yuklab oling:
```bash
git clone [https://github.com/doniyorfayzullayev616-ux/Smart-sklad.git](https:https://github.com/doniyorfayzullayev616-ux/Smart-sklad.git)
cd Smart-Sklad