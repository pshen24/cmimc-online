from django.db import models
from django.utils.translation import ugettext_lazy as _

class Contest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    min_team_size = models.IntegerField() # if we ever need an individual contest,
    max_team_size = models.IntegerField() # set min and max team size to 1
    reg_start_date = models.DateTimeField(help_text=_('The date that registration \
            opens, and mathletes can start forming teams'))
    reg_end_date = models.DateTimeField(help_text=_('Teams can no longer be modified \
            after this date')) 

    def __str__(self):
        return self.name

    # TODO: update for coaches
    # whether the user is registered for this contest
    def is_registered(self, user):
        if not user.is_authenticated:
            return False
        if not user.is_mathlete:
            return False
        return user.has_team(self)

