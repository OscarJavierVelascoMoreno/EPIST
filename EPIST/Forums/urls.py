from django.urls import path
from . import views

urlpatterns = [
    path('forums_list/', views.forums_list, name='forums_list'),
    path('forum_details/<int:id>', views.forum_details, name='forum_details'),
    path('forum_create/', views.forum_create, name='forum_create'),
    path('forum_edit/<int:id>', views.forum_edit, name='forum_edit'),
    path('forum_delete/<int:id>', views.forum_delete, name='forum_delete'),
    path('discussions_list/', views.discussions_list, name='discussions_list'),
    path('discussion_details/<int:id>', views.discussion_details, name='discussion_details'),
    path('discussions_details_list/<int:id>', views.discussions_details_list, name='discussions_details_list'),
    path('discussion_create/<int:id>', views.discussion_create, name='discussion_create'),
    path('discussion_edit/<int:id>', views.discussion_edit, name='discussion_edit'),
    path('discussion_delete/<int:id>', views.discussion_delete, name='discussion_delete'),
    path('message_details/<int:id>', views.message_details, name='message_details'),
    path('message_create/<int:id>', views.message_create, name='message_create'),
    path('message_edit/<int:id>', views.message_edit, name='message_edit'),
    path('message_delete/<int:id>', views.message_delete, name='message_delete'),
    path('create_knowledge/<int:id>', views.create_knowledge, name='create_knowledge'),
    path('relevant_message/<int:id>', views.relevant_message, name='relevant_message'),
]