# Django Stripe API

Приложение на Django + Stripe, позволяющее проводить оплату отдельных товаров (`Item`) и заказов (`Order`), включая поддержку скидок, налогов и разных валют (USD, EUR).  

## Демо

Проект развернут на облачной платформе Render и доступен для тестирования:

* **Сайт:** https://django-stripe-api-q3ya.onrender.com
* **Админ-панель:** https://django-stripe-api-q3ya.onrender.com/admin/

**Доступ к админ-панели:**  
login: admin
password: admin123

## Функциональность

* **Просмотр и покупка Item** - На `/item/{id}/` отображается информация о товаре и кнопка "Buy". Запрос на `/buy/{id}/` получает `session.id` для редиректа на Stripe Checkout. 
* **Просмотр и покупка Order** - На `/order/{id}/` отображается заказ с учетом скидок и налогов. Запрос на `/order/{id}/buy/` инициирует оплату всего заказа. 
* **Мультивалютность** - Полная поддержка **USD** и **EUR**. Ключи Stripe (Public/Secret) и ID скидок/налогов выбираются динамически в зависимости от валюты item/order. 
* **Покупка Order** - возможность оплатить order, объединяющий несколько товаров, через stripe.checkout.Session. 
* **Мультивалютность** - поддержка **USD** и **EUR**. Ключи Stripe (Public/Secret) и ID скидок/налогов выбираются автоматически в зависимости от валюты item/order. 
* **Скидки и Налоги** - применение моделей `Discount` и `Tax` к order. 


## Модели

* **Item**
- name
- description
- price
- currency (USD / EUR)

* **Order**
- список Item
- Discount
- Tax

* **Discount**
- процент скидки
- Stripe coupon id (USD / EUR)

* **Tax**
- процент налога
- Stripe tax rate id (USD / EUR)


## Стек технологий

- **Python**
- **Django**
- **Stripe API**
- **Docker + Docker Compose**
- **PostgreSQL** (Render)
- **Render (деплой)**


## Установка и локальный запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/sonyanyaw/django-stripe-api.git
cd django-stripe-api
```

2. Создать файл .env
```env
DEBUG='True'
SECRET_KEY='django-insecure...'

DB_URL='database_url'
# или
DB_NAME='database_name'
DB_USER='user'           
DB_PASSWORD='password'        
DB_HOST='host'        
DB_PORT='port'

ALLOWED_HOSTS='localhost 127.0.0.1'

CSRF_TRUSTED_ORIGINS='http://localhost http://127.0.0.1'

STRIPE_PUBLIC_KEY_USD='pk_test_xxx'
STRIPE_SECRET_KEY_USD='sk_test_xxx'
STRIPE_PUBLIC_KEY_EUR='pk_test_xxx'
STRIPE_SECRET_KEY_EUR='sk_test_xxx'

DJANGO_SUPERUSER_USERNAME='admin'
DJANGO_SUPERUSER_EMAIL='admin@example.com'
DJANGO_SUPERUSER_PASSWORD='admin123'
```

3. Запуск через Docker
```bash
docker-compose up --build
```

После запуска приложение будет доступно по адресу:
```
http://localhost:8000
```

## API эндпоинты

* **Получить страницу товара**
- GET /item/<id>/

* **Создать Stripe Checkout Session для товара**
- GET /buy/<id>/

* **Получить страницу заказа**
- GET /order/<id>/

* **Создать Stripe Checkout Session для заказа**
- GET /order/<id>/buy/


## Деплой на Render

Проект развёрнут через:
* **Docker**
* **Web Service (Render)**
* **Database PostgreSQL (Render)**