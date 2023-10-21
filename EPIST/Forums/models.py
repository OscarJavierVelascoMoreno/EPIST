from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from datetime import date
from Users.models import User
from Projects.models import Project
from Knowledge.models import Knowledge, KnowledgeStep
from Knowledge.views import knowledge_details
from django.shortcuts import render

FRM_STATE_CHOICES = (
    ("open", "Abierto"),
    ("closed", "Cerrado"),
)

DCS_STATE_CHOICES = (
    ("open", "Abierto"),
    ("closed", "Cerrado"),
)


# Models for forum management.
class Forum(models.Model):

    class Meta:
        verbose_name = "Foro"

    title = models.CharField(max_length=100, unique=True, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    creation_date = models.DateField(default=timezone.now, verbose_name="Fecha de Creación")
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='%(class)s_created', verbose_name="Creado Por")
    state = models.CharField(choices=FRM_STATE_CHOICES, default='open', verbose_name="Estado")
    project_id = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL, verbose_name="Proyecto")

    def __str__(self):
        return self.title

    def close_forum(self):
        self.state = 'closed'


class Discussion(models.Model):

    class Meta:
        verbose_name = "Discusión"

    title = models.CharField(max_length=100, unique=True, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    creation_date = models.DateField(default=timezone.now, verbose_name="Fecha de Creación")
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='%(class)s_created', verbose_name="Creado Por")
    state = models.CharField(choices=DCS_STATE_CHOICES, default='open', verbose_name="Estado")
    forum_id = models.ForeignKey(Forum, null=True, on_delete=models.CASCADE, verbose_name="Foro")
    project_id = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL, verbose_name="Proyecto")

    def __str__(self):
        return self.title

    def close_discussion(self):
        self.state = 'closed'

    def create_knowledge(self):
        new_knowledge = Knowledge.objects.create(
            title = self.title,
            state = 'for_approval',
            project_id = self.project_id,
            note = self.description,
            created_by = self.created_by,
            creation_date = date.today()
        )
        message_ids = self.create_message(new_knowledge)
        return new_knowledge

    def create_message(self, knowledge):
        messages = Message.objects.filter(discussion_id=self.id)
        new_messages = []
        for message in messages:
            if message.mark_relevant:
                new_msg = KnowledgeStep.objects.create(
                    title = message.title,
                    description = message.description,
                    image = message.image,
                    knowledge_id = knowledge,
                    created_by = self.created_by
                )
                new_messages.append(new_msg)


class Message(models.Model):

    class Meta:
        verbose_name = "Mensaje"

    title = models.CharField(max_length=100, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    image = models.ImageField(upload_to='uploads/ForumMessage/', null=True, verbose_name="Imagen")
    creation_date = models.DateField(default=timezone.now, verbose_name="Fecha de Creación")
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name="Creado Por")
    discussion_id = models.ForeignKey(Discussion, on_delete=models.CASCADE, verbose_name="Discusión")
    mark_relevant = models.BooleanField(verbose_name="Marcar como Relevante")

    def __str__(self):
        return self.title
