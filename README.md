# Тестовая реализация Django + Stripe API (бэкенд)
## Сделано:
- Модель Item (name, description, price, picture) с админкой Django.
- Модель Order, объединяет несколько Item в один заказ с общей оплатой.
- Модель Tax / Discounts привязывается к Order, корректно отображается отдельной строкой в Stripe Checkout.
- GET /item/{id}/ — страница товара с кнопкой Buy.
- GET /buy/{id}/ — создаёт Stripe Checkout Session для одного товара.
- GET /order/{id}/ — страница заказа с кнопкой Buy.
- GET /buy_order/{id}/ — создаёт Stripe Checkout Session для всего заказа (с учётом налога, если задан).
- GET /success/, GET /cancel/ — страницы после оплаты/отмены.
- Django Admin — просмотр и редактирование Item/Order/Tax.
- Docker — запуск в контейнере.
- Доступ к удаленке с админкойю

| Backend | Python, Django |
| Платежи | stripe (Python SDK), Stripe Checkout |
| Конфиг | python-dotenv |
| Изображения | Pillow |
| Контейнеризация | Docker |

## Форк ориентирован под render.com и подобные. При старте собирается докер контейнер, нужно задать переменные окружения в настройках сайта. 

## Демо вариант на хосте: https://server-stripe-cnru.onrender.com(открывается пустая страница, нужен сразу переход на админку)

## Запуск на локальном/удаленном хосте (Для удаленного хоста требуется дополнительная настройка IP маршрутизации из контейнера наружу и открытие портов):
BASH:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Установка .env 
PYTHON: 
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
Запуск через докер одной командой, но также нужно установить environment:
docker compose up --build

### Для тестирования оплаты использовать 
Номер: 4242 4242 4242 4242 
Срок: любое будущее число
CVC: любые 3 цифры 
## Структура проекта 
<details> <summary>Развернуть</summary>
├── manage.py
├── settings.py
├── urls.py
├── wsgi.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── shop/
    ├── models.py         
    ├── views.py           
    ├── urls.py
    ├── admin.py
    └── templates/shop/
</details>