from django.urls import path
from.import views


urlpatterns=[
path('order/new',views.new_order,name='new_order'),
path('orders',views.get_orders,name='get_orders'),
path('order/<str:pk>',views.get_order,name='get_order'),
path('orders/<str:pk>/process',views.process_order,name='process_order'),
path('orders/<str:pk>/delete',views.delete_order,name='delete_order'),



]