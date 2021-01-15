from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from website.managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    full_name = models.CharField(max_length=100, help_text=_('full name'))
    alias = models.CharField(max_length=100, blank=True, help_text=_('preferred name'))

    MATHLETE = 'ML'
    STAFF = 'ST'
    COACH = 'CO'
    role_CHOICES = [
        (MATHLETE, 'Contestant'),
        (STAFF, 'CMU Student'),
        (COACH, 'Coach'),     # coaches not implemented yet
    ]
    role = models.CharField(max_length=2, choices=role_CHOICES, default=MATHLETE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.name

    @property
    def name(self):
        if self.alias:
            return self.alias
        elif self.full_name:
            return self.full_name
        else:
            return '{0} {1}'.format(self.first_name, self.last_name)

    @property
    def short_name(self):
        if self.first_name:
            return self.first_name
        else:
            return self.name

    @property
    def is_mathlete(self):
        return self.role == self.MATHLETE

    @property
    def is_coach(self):
        return self.role == self.COACH

    def has_team(self, contest):
        if self.is_mathlete:
            return self.mathlete.teams.filter(contest=contest).exists()
        elif self.is_coach:
            return self.teams.filter(contest=contest).exists()
        else:
            return False

    def can_edit(self, team):
        if self.is_staff:
            return True
        if self.is_coach:
            if self == team.coach:
                return True
        if self.is_mathlete:
            if team.coach == None and team in self.mathlete.teams.all():
                return True
        return False

