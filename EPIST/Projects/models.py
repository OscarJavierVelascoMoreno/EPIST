from django.db import models
from django.utils import timezone
from datetime import date
from Users.models import User

STATE_CHOICES = (
    ("draft", "Draft"),
    ("in_progress", "In Progress"),
    ("closed", "Closed"),
)


# Class for projects
class Project(models.Model):

    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    creation_date = models.DateField(timezone.now)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    state = models.CharField(choices=STATE_CHOICES, default='draft')

    @staticmethod
    def close_project(self):
        self.state = 'closed'

    def __str__(self):
        return self.title


class User(User):
    project_ids = models.ManyToManyField(Project)
