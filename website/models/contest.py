from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class Contest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    min_team_size = models.IntegerField() # if we ever need an individual contest,
    max_team_size = models.IntegerField() # set min and max team size to 1
    reg_start_date = models.DateTimeField(help_text=_('The date that registration \
            opens, and mathletes can start forming teams'))
    reg_end_date = models.DateTimeField(help_text=_('Teams can no longer be modified \
            after this date'))
    end_time = models.DateTimeField() # latest end time of any exam in the contest
    start_time = models.DateTimeField() # earliest start time of any exam in the contest

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

    @cached_property
    def _now(self):
        return timezone.now()

    @cached_property
    def end_time(self): # NOTE: returns reg deadline if no exams are in contest
        temp = self.reg_end_date
        for e in self.exams.all():
            if e.end_time > temp:
                temp = e.end_time
        return temp
    
    @cached_property
    def start_time(self): # NOTE: returns reg deadline if no exams are in contest
        if len(self.exams.all()) == 0:
            temp = self.reg_end_date
        else:
            temp = self.exams.all()[0].start_time
        for e in self.exams.all():
            if e.start_time < temp:
                temp = e.start_time
        return temp

    @cached_property
    def ended(self):
        return self._now > self.end_time

    @cached_property
    def started(self):
        return self._now > self.start_time

    @cached_property
    def ongoing(self):
        return self.started and not self.ended

    @cached_property
    def reg_ended(self):
        return self._now > self.reg_end_date