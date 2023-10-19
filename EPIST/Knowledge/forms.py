from django import forms
from .models import Knowledge, KnowledgeStep, KnowledgeType


# Form information for Projects
class KnowledgeForm(forms.ModelForm):

    class Meta:
        model = Knowledge
        fields = ['title', 'type_id', 'project_id', 'note', 'active']


class KnowledgeStepForm(forms.ModelForm):

    class Meta:
        model = KnowledgeStep
        fields = ['title', 'description', 'image', 'knowledge_id']

    def __init__(self, *args, **kwargs):
        super(KnowledgeStepForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

class KnowledgeTypeForm(forms.ModelForm):

    class Meta:
        model = KnowledgeType
        fields = ['title', 'description']
