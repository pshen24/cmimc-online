from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from datetime import timedelta

class Contest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    min_team_size = models.IntegerField() # if we ever need an individual contest,
    max_team_size = models.IntegerField() # set min and max team size to 1
    reg_deadline = models.DateField()
    is_private = models.BooleanField(default=False)
    locked = models.BooleanField(default=False) # either lock manually, or automatic lock
                                                # 24 hours after the reg deadline



    def __str__(self):
        return self.name

    @cached_property
    def now(self):
        return timezone.now()

    # Assumes there is at least one exam in each contest
    @cached_property
    def end_time(self):
        temp = self.now - timedelta(days=100000) # 300 years in the past
        for e in self.exams.all():
            if e.end_time > temp:
                temp = e.end_time
        return temp
    
    # Assumes there is at least one exam in each contest
    @cached_property
    def start_time(self):
        temp = self.now + timedelta(days=100000) # 300 years in the future
        for e in self.exams.all():
            if e.start_time < temp:
                temp = e.start_time
        return temp

    @cached_property
    def ended(self):
        return self.now > self.end_time

    @cached_property
    def started(self):
        return self.now >= self.start_time

    @cached_property
    def ongoing(self):
        return self.started and not self.ended

    # initializes all Competitors, Scores, and TaskScores
    # ensures exactly one score for each (problem, competitor) pair,
    # and exactly one taskscore for each (task, score) pair
    def finalize_all_teams(self):
        for team in self.teams.all():
            team.unregister() # ensure no duplicates
            team.register()

