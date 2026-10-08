# Python 3.12 ning yengil (slim) versiyasini yuklab olamiz
FROM python:3.12-slim

# Konteyner ichida ishchi papkani (directory) belgilaymiz
WORKDIR /app

# Kompyuteringizdagi requirements.txt faylini konteynerga nusxalaymiz
COPY requirements.txt .

# Kutubxonalarni o'rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# Loyihadagi barcha kodlarni konteynerga nusxalaymiz
COPY . .

# Django serverini port 8000 da ishga tushiramiz
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]