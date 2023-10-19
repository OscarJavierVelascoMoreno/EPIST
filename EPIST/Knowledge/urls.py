from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('knowledge_list/', views.knowledge_list, name='knowledge_list'),
    path('knowledge_details/<int:id>', views.knowledge_details, name='knowledge_details'),
    path('knowledge_create/', views.knowledge_create, name='knowledge_create'),
    path('knowledge_edit/<int:id>', views.knowledge_edit, name='knowledge_edit'),
    path('knowledge_delete/<int:id>', views.knowledge_delete, name='knowledge_delete'),
    path('knowledge_to_approval/<int:id>', views.knowledge_to_approval, name='knowledge_to_approval'),
    path('knowledge_approve/<int:id>', views.knowledge_approve, name='knowledge_approve'),
    path('knowledge_step_details/<int:id>', views.knowledge_step_details, name='knowledge_step_details'),
    path('knowledge_step_create/<int:id>', views.knowledge_step_create, name='knowledge_step_create'),
    path('knowledge_step_edit/<int:id>', views.knowledge_step_edit, name='knowledge_step_edit'),
    path('knowledge_step_delete/<int:id>', views.knowledge_step_delete, name='knowledge_step_delete'),
    path('knowledge_type_details/<int:id>', views.knowledge_type_details, name='knowledge_type_details'),
    path('knowledge_type_create/', views.knowledge_type_create, name='knowledge_type_create'),
    path('knowledge_type_edit/<int:id>', views.knowledge_type_edit, name='knowledge_type_edit'),
    path('knowledge_type_delete/<int:id>', views.knowledge_type_delete, name='knowledge_type_delete'),
    path('knowledge_types_list/', views.knowledge_types_list, name='knowledge_types_list'),
]

urlpatterns += static(settings.MEDIA_URL, documents_root=settings.MEDIA_ROOT)
