from django.db import models
from .problem import Problem
from .competitor import Competitor
from django.utils.translation import ugettext_lazy as _
from website.managers import ScoreManager

class Score(models.Model):
    problem = models.ForeignKey(Problem, related_name='scores', on_delete=models.CASCADE)
    competitor = models.ForeignKey(Competitor, related_name='scores', on_delete=models.CASCADE)
    points = models.FloatField(default=0.0)
    task_scores = models.JSONField(null=True, blank=True, default=list, help_text=_("List of \
            best scores for each task of an optimization round problem"))

    objects = ScoreManager()

    def __str__(self):
        return 'Score: (' + str(self.problem) + ', ' + str(self.competitor) + ') = ' \
                + str(self.points)

    class Meta:
        unique_together = ['problem', 'competitor']


