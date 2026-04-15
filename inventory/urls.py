from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('items/', views.item_list, name='item_list'),
    path('request/<int:item_id>/', views.request_item, name='request_item'),
]