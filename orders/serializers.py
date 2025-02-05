from rest_framework import serializers
from .models import Food, Table, Order


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'name', 'price']


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'number']


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.JSONField()

    class Meta:
        model = Order
        fields = [
            'id', 'table', 'items', 'total_price', 'status', 'created_at', 'is_hidden'
        ]

    def validate_items(self, value):
        # Проверяем, что items — это список словарей с ключами name и price
        if not isinstance(value, list):
            raise serializers.ValidationError("Items must be a list of dictionaries.")
        for item in value:
            if not isinstance(item, dict):
                raise serializers.ValidationError("Each item must be a dictionary.")
            if 'name' not in item or 'price' not in item:
                raise serializers.ValidationError("Each item must contain 'name' and 'price'.")
            if not isinstance(item['price'], (int, float)):
                raise serializers.ValidationError("Price must be a number.")
        return value

    def create(self, validated_data):
        items = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        order.items = [{"name": item['name'], "price": float(item['price'])} for item in items]
        order.save()
        return order
