from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
 
urlpatterns = [
    path('', views.home, name='home'),
    path('items/', views.item_list, name='item_list'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
 
    # Student
    path('request/<int:item_id>/', views.request_item, name='request_item'),
    path('my_requests/', views.my_requests, name='my_requests'),
    path('my_items/', views.my_items, name='my_items'),
    path('return/<int:request_id>/', views.return_item, name='return_item'),
 
    # Staff
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('manage_requests/', views.manage_requests, name='manage_requests'),
    path('approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('add_stock/<int:item_id>/', views.add_stock, name='add_stock'),
 
    # Manager
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('items/add/', views.add_item, name='add_item'),
    path('items/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('items/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('all_requests/', views.all_requests, name='all_requests'),
    path('export_requests/', views.export_requests_csv, name='export_requests_csv'),
    
    
    # Admin
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
 