from django.db import models
from .problem import Problem
from .competitor import Competitor
from .task import Task
from .score import Score
from django.utils.translation import ugettext_lazy as _

class Submission(models.Model):
    problem = models.ForeignKey(Problem, related_name='submissions', on_delete=models.CASCADE)
    competitor = models.ForeignKey(Competitor, related_name='submissions', \
            on_delete=models.CASCADE)
    points = models.FloatField(null=True, blank=True)
    is_graded = models.BooleanField(default=False)
    text = models.TextField(help_text=_('The string that the competitor submitted. \
            Its format depends on the exam (can be an integer, source code, \
            program output, etc)'))
    submit_time = models.DateTimeField(auto_now_add=True, db_index=True)
    task = models.ForeignKey(Task, related_name="submissions", on_delete=models.CASCADE, \
            null=True, blank=True) # only for optimization
    # add something for errors? (if they submit something invalid)

    def __str__(self):
        return str(self.competitor) + "'s submission to problem " + str(self.problem)

    def grade(self):
        score = Score.objects.get(problem=self.problem, competitor=self.competitor)
        self.problem.grader.grade(self, score)

    def can_view(self, user):
        if user.is_staff:
            return True
        if user.is_coach and user == self.competitor.team.coach:
            return True
        if user.is_mathlete:
            comp = Competitor.objects.getCompetitor(self.problem.exam, user.mathlete)
            if comp == self.competitor:
                return True
        return False
