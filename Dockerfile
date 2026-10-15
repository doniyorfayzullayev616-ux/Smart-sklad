# Python 3.12 ning yengil (slim) versiyasini yuklab olamiz
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Konteyner ichida ishchi papkani (directory) belgilaymiz
WORKDIR /app

# Kompyuteringizdagi requirements.txt faylini konteynerga nusxalaymiz
COPY requirements.txt /app/


# Kutubxonalarni o'rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# Loyihadagi barcha kodlarni konteynerga nusxalaymiz
COPY . /app/

RUN useradd -m sklad_user

RUN chown -R sklad_user:sklad_user /app

USER sklad_user

EXPOSE 8000
# Django serverini port 8000 da ishga tushiramiz
CMD ["gunicorn", "Store_Flow.wsgi:application", "--bind", "0.0.0.0:8000"]