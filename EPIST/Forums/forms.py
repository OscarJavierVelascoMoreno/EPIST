from django import forms
from .models import Forum, Discussion, Message


# Form information for Projects
class ForumForm(forms.ModelForm):

    class Meta:
        model = Forum
        fields = ['title', 'description', 'project_id']


class DiscussionForm(forms.ModelForm):

    class Meta:
        model = Discussion
        fields = ['title', 'description', 'forum_id', 'project_id']


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['description', 'discussion_id', 'mark_relevant']
