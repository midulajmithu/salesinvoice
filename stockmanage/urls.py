"""
URL configuration for salesinvoice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
urlpatterns = [
    path('home/',views.dashboard,name='home'),
    path('purchase/',views.purchase,name='purchase'),
    path('stockmovement/',views.stockmovement,name='sale'),
    path('stock/',views.stock,name='stock'),
    path('delete/<int:id>/', views.delete_entry, name='delete_entry'),
    path('export/<str:record_type>/', views.export_to_excel, name='export_to_excel'),
    path('admin_export/<str:record_type>/<str:user_id>/', views.admin_export_to_excel, name='admin_export_to_excel'),
    path('analysis/', views.analysis, name='analysis'),
    path('update_entry/', views.update_entry, name='update_entry'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_purchase/<str:user_id>/', views.purchase_admin, name='purchase_admin'),
    path('admin_stockmovement/<str:user_id>/', views.stock_movement_admin, name='stockmovement_admin'),
    path('admin_stock/<str:user_id>/', views.admin_stock, name='stock_admin'),
    path('api/get-stock-quantity/', views.get_stock_quantity, name='get_stock_quantity'),
    path('admin_analysis/<str:user_id>/', views.admin_analysis, name='analysis_admin')

]
