from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class Contest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    min_team_size = models.IntegerField() # if we ever need an individual contest,
    max_team_size = models.IntegerField() # set min and max team size to 1
    reg_end_date = models.DateTimeField(help_text=_('Teams can no longer be modified \
            after this date'))
    is_private = models.BooleanField(default=False)


    def __str__(self):
        return self.name

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

    # initializes all Competitors, Scores, and TaskScores
    # ensures exactly one score for each (problem, competitor) pair,
    # and exactly one taskscore for each (task, score) pair
    def finalize_all_teams(self):
        for team in self.teams.all():
            team.unregister() # ensure no duplicates
            team.register()

