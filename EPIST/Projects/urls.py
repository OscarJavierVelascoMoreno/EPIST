from django.urls import path
from . import views

urlpatterns = [
    path('projects_list/', views.projects_list, name='projects_list'),
    path('project_details/<int:id>', views.project_details, name='project_details'),
    path('project_create/', views.project_create, name='project_create'),
    path('project_edit/<int:id>', views.project_edit, name='project_edit'),
    path('project_delete/<int:id>', views.project_delete, name='project_delete'),
]