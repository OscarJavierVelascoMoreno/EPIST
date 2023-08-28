from django.urls import path
from . import views

urlpatterns = [
    path('base_view/', views.baseView, name='base_view'),
    path('welcome/', views.welcome, name='welcome'),
    path('users_list/', views.users_list, name='users_list'),
    path('user_details/<int:id>', views.user_details, name='user_details'),
    path('user_create/', views.user_create, name='user_create'),
    path('user_edit/<int:id>', views.user_edit, name='user_edit'),
    path('user_delete/<int:id>', views.user_delete, name='user_delete'),
    path('user_change_password/<int:id>', views.user_change_password, name='user_change_password'),
]