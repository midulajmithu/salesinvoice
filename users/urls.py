# urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('sign-up/', views.sign_up, name='sign_up'),
    path('logout/', views.custom_logout, name='logout'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('admin_add_user/', views.admin_useradd, name='admin_add_user'),
    path('user_list/', views.user_list, name='user_list'),
    path('update_user/', views.update_user, name='update_user'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('set_inactive/<int:user_id>/', views.set_inactive, name='set_inactive'),

]
