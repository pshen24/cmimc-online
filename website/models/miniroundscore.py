from django.db import models
from .score import Score

# Only used for AI Round
class MiniRoundScore(models.Model):
    score = models.ForeignKey(Score, related_name="miniroundscores", on_delete=models.CASCADE)
    miniround = models.IntegerField()
    points = models.FloatField(default=0.0)

