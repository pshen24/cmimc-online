from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from website.managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
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
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.preferred_name

    @property
    def preferred_name(self):
        if self.alias:
            return self.alias
        return self.full_name

    @property
    def is_mathlete(self):
        return self.role == self.MATHLETE

    @property
    def is_coach(self):
        return self.role == self.COACH

    def has_team(self, contest):
        if self.is_staff:
            return False
        elif self.is_mathlete:
            return self.mathlete.teams.filter(contest=contest).exists()
        else:
            return self.teams.filter(contest=contest).exists()


