from django.test import TestCase
from .models import Food, Table, Order
from rest_framework.test import APIClient
from django.urls import reverse


class OrderModelTest(TestCase):
    def setUp(self):
        self.food = Food.objects.create(name="Гамбургер", price=10.99)
        self.table = Table.objects.create(number=1)
        self.order = Order.objects.create(
            table=self.table,
            items=[{"name": self.food.name, "price": float(self.food.price)}],
            status="waiting"
        )

    def test_order_creation(self):
        self.assertEqual(self.order.total_price, 10.99)
        self.assertEqual(self.order.service_fee, 1.10)
        self.assertEqual(self.order.total_with_service, 12.09)


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.food = Food.objects.create(name="Гамбургер", price=10.99)
        self.table = Table.objects.create(number=1)
        self.order = Order.objects.create(
            table=self.table,
            items=[{"name": self.food.name, "price": float(self.food.price)}],
            status="waiting"
        )

    def test_order_list_api(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)