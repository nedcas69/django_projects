from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.contrib import messages
from datetime import datetime, date
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Food, Table
from .forms import OrderForm
from .serializers import FoodSerializer, TableSerializer, OrderSerializer


# Клиентские представления
def client_dashboard(request):
    try:
        query = request.GET.get('q')
        if query:
            orders = Order.objects.filter(id__icontains=query) | Order.objects.filter(table__number__icontains=query)
        else:
            orders = None
        foods = Food.objects.all()
        return render(request, 'orders/client_dashboard.html', {'foods': foods, 'orders': orders})
    except Exception as e:
        messages.error(request, f"Ошибка: {str(e)}")
        return redirect('client_dashboard')


def cancel_order_by_client(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id)
        if order.status == 'waiting':
            order.status = 'canceled'
            order.save()
            messages.success(request, "Заказ успешно отменен.")
            return redirect('client_dashboard')
        else:
            messages.error(request, "Невозможно отменить заказ, так как он уже готов или оплачен.")
    except Exception as e:
        messages.error(request, f"Ошибка: {str(e)}")
    return redirect('client_dashboard')


def order_detail(request, pk):
    try:
        order = get_object_or_404(Order, pk=pk)
        return render(request, 'orders/order_detail.html', {'order': order})
    except Exception as e:
        messages.error(request, f"Ошибка: {str(e)}")
        return redirect('client_dashboard')


def create_order(request):
    try:
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                table = form.cleaned_data['table']
                items = form.cleaned_data['items']
                order_items = [{"name": item.name, "price": float(item.price)} for item in items]
                Order.objects.create(table=table, items=order_items)
                messages.success(request, "Заказ успешно создан.")
                return redirect('client_dashboard')
        else:
            form = OrderForm()
        return render(request, 'orders/create_order.html', {'form': form})
    except Exception as e:
        messages.error(request, f"Ошибка: {str(e)}")
        return redirect('client_dashboard')


def edit_order(request, pk):
    try:
        order = get_object_or_404(Order, pk=pk)
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order.table = form.cleaned_data['table']
                items = form.cleaned_data['items']
                order.items = [{"name": item.name, "price": float(item.price)} for item in items]
                order.save()
                messages.success(request, "Заказ успешно обновлен.")
                return redirect('client_dashboard')
        else:
            initial_data = {
                'table': order.table,
                'items': [item['name'] for item in order.items],
            }
            form = OrderForm(initial=initial_data)
        return render(request, 'orders/edit_order.html', {'form': form, 'order': order})
    except Exception as e:
        messages.error(request, f"Ошибка: {str(e)}")
        return redirect('client_dashboard')


# Операторские представления
def operator_dashboard(request):
    try:
        new_orders = Order.objects.filter(status='waiting', is_hidden=False).prefetch_related('table')
        canceled_orders = Order.objects.filter(status='canceled', is_hidden=False).prefetch_related('table')
        ready_orders = Order.objects.filter(status='ready').prefetch_related('table')
        return render(request, 'orders/operator_dashboard.html', {
            'new_orders': new_orders,
            'canceled_orders': canceled_orders,
            'ready_orders': ready_orders,
        })
    except Exception as e:
        messages.error(request, f"Ошибка: {str(e)}")
        return redirect('operator_dashboard')


def mark_order_ready(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id)
        order.status = 'ready'
        order.save()
        messages.success(request, "Статус заказа изменен на 'Готово'.")
        return redirect('operator_dashboard')
    except Exception as e:
        messages.error(request, f"Ошибка: {str(e)}")
    return redirect('operator_dashboard')


def mark_order_paid(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id)
        order.status = 'paid'
        order.save()
        messages.success(request, "Статус заказа изменен на 'Оплачено'.")
        return redirect('operator_dashboard')
    except Exception as e:
        messages.error(request, f"Ошибка: {str(e)}")
    return redirect('operator_dashboard')


def hide_canceled_order(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id, status='canceled')
        order.is_hidden = True
        order.save()
        messages.success(request, "Заказ успешно скрыт.")
        return redirect('operator_dashboard')
    except Exception as e:
        messages.error(request, f"Ошибка: {str(e)}")
    return redirect('operator_dashboard')


def update_order_status(request, pk, status):
    try:
        order = get_object_or_404(Order, pk=pk)
        if status in ['ready', 'paid']:
            order.status = status
            order.save()
        messages.success(request, "Заказ успешно обновлён.")
        return redirect('operator_dashboard')
    except Exception as e:
        messages.error(request, f"Ошибка: {str(e)}")
        return redirect('operator_dashboard')


def paid_orders_report(request):
    try:
        today = date.today()
        today_total = Order.objects.filter(
            status='paid', created_at__date=today
        ).aggregate(total=Sum('total_price'))['total'] or 0
        paid_orders = Order.objects.filter(status='paid').order_by('-created_at')
        paginator = Paginator(paid_orders, 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'orders/paid_orders_report.html', {
            'today_total': today_total,
            'page_obj': page_obj,
        })
    except Exception as e:
        messages.error(request, f"Ошибка: {str(e)}")
        return redirect('operator_dashboard')


# API представления
@api_view(['GET', 'POST'])
def api_food_list(request):
    if request.method == 'GET':
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def api_food_detail(request, pk):
    try:
        food = Food.objects.get(pk=pk)
    except Food.DoesNotExist:
        return Response({"error": "Food not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FoodSerializer(food)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = FoodSerializer(food, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        food.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def api_order_list(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def api_order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
