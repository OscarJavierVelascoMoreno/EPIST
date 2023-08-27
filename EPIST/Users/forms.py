from django import forms
from Projects.models import Project, User


# Form information for Users
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'ident_number', 'email', 'username', 'project_ids']

    project_ids = forms.ModelMultipleChoiceField(
        queryset=Project.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
