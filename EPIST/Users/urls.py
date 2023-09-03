from django.urls import path, include
from . import views

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('accounts/login/', views.page_login, name='login'),
    path('logout/', views.page_logout, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('users_list/', views.users_list, name='users_list'),
    path('user_details/<int:id>', views.user_details, name='user_details'),
    path('user_create/', views.user_create, name='user_create'),
    path('user_edit/<int:id>', views.user_edit, name='user_edit'),
    path('user_delete/<int:id>', views.user_delete, name='user_delete'),
    path('user_change_password/<int:id>', views.user_change_password, name='user_change_password'),
]