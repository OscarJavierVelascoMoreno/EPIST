from django import forms
from .models import Knowledge, KnowledgeStep


# Form information for Projects
class KnowledgeForm(forms.ModelForm):

    class Meta:
        model = Knowledge
        fields = ['title', 'type_id', 'project_id', 'note', 'active']


class KnowledgeStepForm(forms.ModelForm):

    class Meta:
        model = KnowledgeStep
        fields = ['title', 'description']
