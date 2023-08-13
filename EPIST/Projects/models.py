from django.db import models
from Users.models import User

STATE_CHOICES = (
    ("draft", "Draft"),
    ("in_progress", "In Progress"),
    ("closed", "Closed"),
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

    def __str__(self):
        return self.name


class User(User):
    project_ids = models.ManyToManyField(Project)

    def __str__(self):
        return self.name
