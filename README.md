# 📦 Smart-Sklad API

Smart-Sklad — bu do'kon va omborxonalar uchun mahsulotlarni boshqarishga mo'ljallangan ishonchli va xavfsiz RESTful API tizimi. Loyiha biznes ehtiyojlarini hisobga olgan holda ishlab chiqilgan va to'liq Docker muhitiga qadoqlangan.

## 🚀 Asosiy Imkoniyatlar (Features)

* **To'liq CRUD:** Mahsulotlar va kategoriyalarni qo'shish, o'qish, tahrirlash va o'chirish.
* **Xavfsizlik (Authentication):** JWT (JSON Web Tokens) orqali ishonchli avtorizatsiya va ruxsatlarni boshqarish tizimi.
* **Qidiruv va Filtrlash:** Mahsulotlarni nomi va xususiyatlari bo'yicha tezkor qidirish imkoniyati (`SearchFilter`).
* **Hisobot (Export):** Ombor qoldiqlarini Excel (CSV) formatida ko'chirib olish funksiyasi.
* **Konteynerizatsiya:** Docker va Docker Compose orqali istalgan operatsion tizimda bitta buyruq bilan xatosiz ishga tushirish.

## 🛠 Texnologiyalar (Tech Stack)

* **Dasturlash tili:** Python 3.12
* **Backend:** Django, Django REST Framework
* **Avtorizatsiya:** djangorestframework-simplejwt
* **Ma'lumotlar bazasi:** SQLite
* **Infratuzilma:** Docker, Docker Compose

## ⚙️ Loyihani ishga tushirish

Loyihani kompyuteringizda yurgizish uchun Docker o'rnatilgan bo'lishi kerak. 

1. Repozitoriyani kompyuterga yuklab oling:
```bash
git clone [https://github.com/SIZNING-LOGININGIZ/Smart-Sklad.git](https://github.com/SIZNING-LOGININGIZ/Smart-Sklad.git)
cd Smart-Sklad