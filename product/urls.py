from django.urls import path
from.import views


urlpatterns=[
path('products/',views.get_all_prodects,name='products'),
path('products/<str:pk>',views.get_by_id_product,name='get_by_id_product'),
path('product/new', views.new_product, name='new_product'),
path('products/updata/<str:pk>',views.updata_product,name='updata_product'),
path('products/delete/<str:pk>',views.delete_product,name='delete_product'),


path('<str:pk>/reviews',views.create_review,name='create_review'),



 ] 