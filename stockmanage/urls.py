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
    path('home/',views.dashbord,name='home'),
    path('purchase/',views.purchase,name='purchase'),
    path('stockmovement/',views.stockmovement,name='sale'),
    path('stock/',views.stock,name='stock'),
    path('delete/<int:id>/', views.delete_entry, name='delete_entry'),
    path('export/<str:record_type>/', views.export_to_excel, name='export_to_excel'),
    path('analysis/', views.analysis, name='analysis'),
    path('update_entry/', views.update_entry, name='update_entry')

]
