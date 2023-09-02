from django import forms
from .models import Project


# Form information for Projects
class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['state', 'title', 'description']

