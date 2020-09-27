from django.contrib.auth.forms import UserCreationForm as DefaultUserCreationForm
from django.contrib.auth.forms import UserChangeForm as DefaultUserChangeForm
from website.models import User


class UserCreationForm(DefaultUserCreationForm):
    class Meta(DefaultUserCreationForm):
        model = User
        fields = ('email', 'full_name', 'alias', 'role')


class UserChangeForm(DefaultUserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'alias', 'role')
