from django.urls import path
from . import views

urlpatterns = [
    # Клиентские маршруты
    path('', views.client_dashboard, name='client_dashboard'),
    path('create/', views.create_order, name='create_order'),
    path('edit/<int:pk>/', views.edit_order, name='edit_order'),
    path('cancel/<int:order_id>/', views.cancel_order_by_client, name='cancel_order_by_client'),

    # Операторские маршруты
    path('operator/', views.operator_dashboard, name='operator_dashboard'),
    path('mark-ready/<int:order_id>/', views.mark_order_ready, name='mark_order_ready'),
    path('mark-paid/<int:order_id>/', views.mark_order_paid, name='mark_order_paid'),
    path('hide-canceled/<int:order_id>/', views.hide_canceled_order, name='hide_canceled_order'),
    path('paid-orders/', views.paid_orders_report, name='paid_orders_report'),
    path('<int:pk>/update-status/<str:status>/', views.update_order_status, name='update_order_status'),

    # API маршруты
    path('api/foods/', views.api_food_list, name='api_food_list'),
    path('api/foods/<int:pk>/', views.api_food_detail, name='api_food_detail'),
    path('api/orders/', views.api_order_list, name='api_order_list'),
    path('api/orders/<int:pk>/', views.api_order_detail, name='api_order_detail'),
]
