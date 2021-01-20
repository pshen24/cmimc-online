from django.db import models
from .task import Task
from .score import Score

# Only used for optimization problems
class TaskScore(models.Model):
    task = models.ForeignKey(Task, related_name="taskscores", on_delete=models.CASCADE)
    score = models.ForeignKey(Score, related_name="taskscores", on_delete=models.CASCADE)
    raw_points = models.FloatField(default=0.0)     # score from grader
    norm_points = models.FloatField(default=0.0)    # normalized score
