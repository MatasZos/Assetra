from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('items/', views.item_list, name='item_list'),
    path('request/<int:item_id>/', views.request_item, name='request_item'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    
    
    
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('add_stock/<int:item_id>/', views.add_stock, name='add_stock'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('manage_requests/', views.manage_requests, name='manage_requests'),
    path('approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('add_stock/<int:item_id>/', views.add_stock, name='add_stock'),
]
