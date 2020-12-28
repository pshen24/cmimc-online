from django.contrib.auth.forms import UserCreationForm as DefaultUserCreationForm
from django.contrib.auth.forms import UserChangeForm as DefaultUserChangeForm
from website.models import User
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

class EditorForm(forms.Form):
    text = forms.CharField(
        widget=AceWidget(
            mode='python',
            theme='xcode',
            fontsize='18px',
            width="100%",
            height="50vh",
            toolbar=False,
        ),
        label='Code Here!',
        required=False,
    )

class ViewOnlyEditorForm(forms.Form):
    text = forms.CharField(
        widget=AceWidget(
            mode='python',
            theme='katzenmilch',
            fontsize='18px',
            width="100%",
            height="50vh",
            toolbar=False,
            readonly=True,
            showgutter=False,
        ),
        label='Note: Read-Only!',
        required=False,
    )