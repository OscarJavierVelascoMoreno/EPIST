from django.db import models
from django.utils import timezone
from datetime import date
from Users.models import User

STATE_CHOICES = (
    ("draft", "Borrador"),
    ("in_progress", "En Progreso"),
    ("closed", "Cerrado"),
)


# Class for projects
class Project(models.Model):

    title = models.CharField(max_length=100, unique=True, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    creation_date = models.DateField(default=timezone.now, verbose_name="Fecha de Creación")
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name="Creado Por")
    state = models.CharField(choices=STATE_CHOICES, default='draft', verbose_name="Estado")

    @staticmethod
    def close_project(self):
        self.state = 'closed'

    def __str__(self):
        return self.title


class User(User):
    project_ids = models.ManyToManyField(Project, verbose_name="Proyectos")
