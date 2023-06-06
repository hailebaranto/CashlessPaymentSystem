from django.urls import path
from . import views

app_name = 'PointOfSale'

urlpatterns = [
    path('', views.index, name='index'),
    path('transaction/', views.transaction_view, name='transaction'),
    path('shops/', views.shop_list, name='shop_list'),
    path('users/', views.user_list, name='user_list'),
]
