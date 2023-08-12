from django.db import models
from Users.models import User

STATE_CHOICES = (
    ("draft", "Borrador"),
    ("in_progress", "En Progreso"),
    ("closed", "Cerrado"),
)

# Class for projects
class Project(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateField()
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    state = models.CharField(choices=STATE_CHOICES, default='draft')

    @staticmethod
    def close_project(self):
        self.state = 'closed'
