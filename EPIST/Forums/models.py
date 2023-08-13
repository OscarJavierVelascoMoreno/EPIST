from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from datetime import date
from Users.models import User
from Projects.models import Project
from Knowledge.models import Knowledge, KnowledgeStep

FRM_STATE_CHOICES = (
    ("open", "Open"),
    ("closed", "Closed"),
)

DCS_STATE_CHOICES = (
    ("open", "Open"),
    ("closed", "Closed"),
)


# Models for forum management.
class Forum(models.Model):

    title = models.CharField(max_length=100, unique=True)
    description = RichTextField()
    creation_date = models.DateField(timezone.now)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='%(class)s_created')
    state = models.CharField(choices=FRM_STATE_CHOICES, default='open')
    project_id = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    def close_forum(self):
        self.state = 'closed'


class Discussion(models.Model):

    title = models.CharField(max_length=100, unique=True)
    description = RichTextField()
    creation_date = models.DateField(timezone.now)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='%(class)s_created')
    state = models.CharField(choices=DCS_STATE_CHOICES, default='open')
    forum_id = models.ForeignKey(Forum, null=True, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)

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
            partner_ids = self.created_by,
            creation_date = date.today()
        )
        message_ids = self.create_message(new_knowledge)

    def create_message(self, knowledge):
        messages = Message.objects.filter(discussion_id=self.id)
        new_messages = []
        for message in messages:
            new_msg = KnowledgeStep.objects.create(
                title = message.title,
                description = message.description,
                knowledge_id = knowledge,
                created_by = self.created_by
            )
            new_messages.append(new_msg)


class Message(models.Model):

    title = models.CharField(max_length=100)
    description = RichTextField()
    creation_date = models.DateField(timezone.now)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    discussion_id = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    mark_relevant = models.BooleanField()

    def __str__(self):
        return self.title
