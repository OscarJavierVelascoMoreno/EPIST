from django.db import models
from ckeditor.fields import RichTextField
from datetime import date
from Users.models import User
from Projects.models import Project

KNL_STATE_CHOICES = (
    ("new", "New"),
    ("for_approval", "For Approval"),
    ("approved", "Approved"),
    ("archived", "Archived"),
)


# Models for Knowledge management
class KnowledgeType(models.Model):

    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Knowledge(models.Model):

    title = models.CharField(max_length=100, unique=True)
    state = models.CharField(choices=KNL_STATE_CHOICES, default='new')
    type_id = models.ForeignKey(KnowledgeType, null=True, on_delete=models.SET_NULL)
    project_id = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)
    note = RichTextField()
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='%(class)s_created')
    approved_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='%(class)s_approved')
    partner_ids = models.ManyToManyField(User)
    creation_date = models.DateField(default=date.today())
    approved_date = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def approve_knowledge(self):
        self.state = 'approved'
        self.approved_date = date.today()

    def archive_record(self):
        self.state = 'archived'
        self.active = False

    def __str__(self):
        return self.title


class KnowledgeStep(models.Model):

    title = models.CharField(max_length=100)
    description = RichTextField()
    knowledge_id = models.ForeignKey(Knowledge, on_delete=models.CASCADE)
    creation_date = models.DateField(default=date.today())
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
