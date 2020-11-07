from django.contrib.auth.forms import UserCreationForm as DefaultUserCreationForm
from django.contrib.auth.forms import UserChangeForm as DefaultUserChangeForm
from website.models import User
from website.models import Snippet
from django import forms
from django_ace import AceWidget


class UserCreationForm(DefaultUserCreationForm):
    class Meta(DefaultUserCreationForm):
        model = User
        fields = ('email', 'full_name', 'alias', 'role')


class UserChangeForm(DefaultUserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'alias', 'role')

class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        widgets = {"text": AceWidget(mode='html', theme='twilight'),}
        exclude = ()
