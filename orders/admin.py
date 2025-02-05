from django.contrib import admin
from .models import Food, Table, Order


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'status', 'total_price', 'total_with_service')
    list_filter = ('status',)
    search_fields = ('table__number',)