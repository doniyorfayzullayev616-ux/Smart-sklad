# 📦 Smart-Sklad - Ombor va Kassa Boshqaruv Tizimi

Smart-Sklad — bu do'kon va omborxonalar uchun mahsulotlarni, kassa jarayonlarini va ombor qoldiqlarini boshqarishga mo'ljallangan ishonchli, xavfsiz va to'liq avtomatlashtirilgan tizim. Loyiha zamonaviy biznes ehtiyojlarini hisobga olgan holda ishlab chiqilgan va Docker muhitiga qadoqlangan.

## 🚀 Asosiy Imkoniyatlar (Features)

- **AI Kunlik Tahlilchi (Gemini):** Sun'iy intellekt orqali kunlik savdolar va ombor qoldiqlari bo'yicha avtomatik biznes-tahlil va xulosalar.
- **Xavfsiz Avtorizatsiya (Cookie JWT):** XSS hujumlaridan 100% himoyalangan, JWT tokenlarni faqat `HttpOnly` cookie'larda saqlovchi zamonaviy xavfsizlik tizimi.
- **Ma'lumotlar Butunligi (Soft Delete):** Mahsulotlarni bazadan butunlay o'chirib yubormasdan "Arxivlash" (is_active) orqali kassa tarixini saqlab qolish mantiqi.
- **Kassa va Tranzaksiyalar:** Kassa jarayonlarida xatoliklarni oldini olish uchun `transaction.atomic` yordamida ishonchli savdo amaliyotlari.
- **Optimallashtirilgan API:** Katta hajmdagi ma'lumotlar serverni qotirib qo'ymasligi uchun Pagination va SearchFilter.
- **Interaktiv UI:** Vanilla JavaScript va Fetch API orqali sahifani yangilamasdan ishlaydigan tezkor (SPA uslubidagi) frontend qismi.
- **Hisobot (Export):** Ombor qoldiqlarini Excel (CSV) formatida ko'chirib olish.

## 🛠 Texnologiyalar (Tech Stack)

- **Backend:** Python 3.12, Django, Django REST Framework
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Ma'lumotlar bazasi:** PostgreSQL 15
- **Avtorizatsiya:** djangorestframework-simplejwt (HttpOnly Cookie)
- **Sun'iy Intellekt:** Google Gemini API
- **Infratuzilma:** Docker, Docker Compose

## ⚙️ Loyihani ishga tushirish (Local deployment)

Loyihani kompyuteringizda yurgizish uchun Docker va Docker Compose o'rnatilgan bo'lishi kerak. Boshqa hech qanday dastur yoki Python kutubxonasi talab etilmaydi.

1. Repozitoriyani kompyuterga yuklab oling:
```bash
git clone [https://github.com/doniyorfayzullayev616-ux/Smart-sklad.git](https:https://github.com/doniyorfayzullayev616-ux/Smart-sklad.git)
cd Smart-Sklad