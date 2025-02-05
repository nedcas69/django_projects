from decimal import Decimal
from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название блюда')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return f"{self.name} - {self.price}"


class Table(models.Model):
    number = models.IntegerField(unique=True, verbose_name='Номер стола')

    def __str__(self):
        return f"Стол #{self.number}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
        ('canceled', 'Отменен'),
    ]
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name='Стол')
    items = models.JSONField(verbose_name='Заказанные блюда', default=list)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость', default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_hidden = models.BooleanField(default=False, verbose_name='Скрыт')

    def __str__(self):
        return f"Заказ #{self.id} (Стол {self.table.number})"

    def save(self, *args, **kwargs):
        self.total_price = sum(item['price'] for item in self.items)
        super().save(*args, **kwargs)

    @property
    def service_fee(self):
        return round(self.total_price * Decimal('0.1'), 2)

    @property
    def total_with_service(self):
        return round(self.total_price + self.service_fee, 2)