from django import forms
from Projects.models import User
from django.contrib.auth.models import Group


# Form information for Users
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'ident_number', 'email', 'username', 'password']


# Form information for Users Groups
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
