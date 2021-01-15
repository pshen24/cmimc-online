from django.db import models
from .problem import Problem
from .competitor import Competitor
from django.utils.translation import ugettext_lazy as _

class Score(models.Model):
    problem = models.ForeignKey(Problem, related_name='scores', on_delete=models.CASCADE)
    competitor = models.ForeignKey(Competitor, related_name='scores', on_delete=models.CASCADE)
    points = models.FloatField(default=0.0)

    def __str__(self):
        return 'Score: (' + str(self.problem) + ', ' + str(self.competitor) + ') = ' \
                + str(self.points)

    class Meta:
        unique_together = ['problem', 'competitor']


