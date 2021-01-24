from django.db import models
from .score import Score

# Only used for AI Round
class MiniRoundScore(models.Model):
    score = models.ForeignKey(Score, related_name="miniroundscores", on_delete=models.CASCADE)
    miniround = models.IntegerField()
    points = models.FloatField(default=0.0)

    def __str__(self):
        return 'points={0}, mr={1}, game={2}'.format(str(self.points), str(self.miniround), str(self.score.problem))
