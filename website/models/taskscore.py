from django.db import models
from .task import Task
from .score import Score

# Only used for optimization problems
class TaskScore(models.Model):
    task = models.ForeignKey(Task, related_name="taskscores", on_delete=models.CASCADE)
    score = models.ForeignKey(Score, related_name="taskscores", on_delete=models.CASCADE)
    raw_points = models.FloatField(null=True, blank=True)     # score from grader
    norm_points = models.FloatField(default=0.0)    # normalized score

    class Meta:
        unique_together = ['task', 'score']

    @property
    def display_raw_points(self):
        g = self.task.problem.grader
        return g.rawToString(self.raw_points)

    def __str__(self):
        return '{0}, {1}, raw={2}, norm={3}'.format(str(self.task), str(self.score.competitor.name), str(self.raw_points), str(self.norm_points))

