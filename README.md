# Система управления заказами в кафе

## Описание
Веб-приложение для управления заказами в кафе, разработанное на Django.

## Функциональность страницы клиента
- Просмотр меню.
- Поиск заказов по номеру стола или ID. 
- Добавление, удаление, редактирование и просмотр заказов.


## Страница оператора
- Просмотр и изменения сотояния на "готово" новых заказов.
- Автоматический расчет общей стоимости заказа.
- Просмотр и изменения сотояния на "Оплачено" готовых заказов.
- Просмотр отмененных заказов. удаления их из списка, но в бд остаются информации о заказе. 
- Просмотр оплаченных заказов.
- Расчет выручки за смену.

## Страница admin
- Добавление/удаление/редактирование блюд, столов, заказов

## CRUD через API
- GET /api/orders/ : Получение списка всех заказов.
- POST /api/orders/ : Создание нового заказа.
- GET /api/orders/{id}/ : Получение информации о конкретном заказе.
- PUT/PATCH /api/orders/{id}/ : Обновление информации о заказе.
- DELETE /api/orders/{id}/ : Удаление заказа.

## Стек технологий
- Python 3.9
- Django 4.2.18
- Djangorestframework 3.15.2
- HTML/Bootstrap
- SQLite

## Установка
1. Клонируйте репозиторий.
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Запуск
   ```bash
      cd cafe_order_system
      python manage.py runser
   ```
## Линки
http://127.0.0.1:8000/admin - Админка
http://127.0.0.1:8000/orders - Клиентская часть
http://127.0.0.1:8000/orders/operator - Операторская часть
http://127.0.0.1:8000/orders/api/orders - API orders
http://127.0.0.1:8000/orders/api/foods -API foods

