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
        fields = ['title', 'description']


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['title', 'description', 'mark_relevant', 'image', 'discussion_id']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
