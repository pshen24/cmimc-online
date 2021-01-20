from django.db import models
from .team import Team
from .competitor import Competitor
from .problem import Problem



class AIGrader(models.Model):
    hostname = models.TextField() # hostname of the grader
    currently = models.TextField() # current status of the grader
    class Meta:
        db_table = "graders_airound"


class AIProblem(models.Model):
    code = models.TextField() # python grading code for the contest
    problem = models.ForeignKey(Problem, related_name="aiproblem", on_delete=models.CASCADE)
    numplayers = models.IntegerField() # if numplayers == -1, the game can have a variable number of players. Otherwise, numplayers is constant
    class Meta:
        db_table = "contests_airound"


class AIGame(models.Model):
    """
    0 = in queue
    1 = running
    2 = graded
    """
    status = models.IntegerField(default=0)
    history = models.JSONField(null=True, blank=True) # after the game is played, gives the history output of the grader
    time = models.TimeField() # when the game should be played
    numplayers = models.IntegerField() # number of players
    problem = models.ForeignKey(AIProblem, on_delete=models.CASCADE) # which problem to use
    worker = models.ForeignKey(AIGrader, null=True, blank=True, on_delete=models.SET_NULL) # which grader was used to grade this
    class Meta:
        db_table = "games_airound"


class AISubmission(models.Model):
    game = models.ForeignKey(AIGame, on_delete=models.CASCADE) # game that submission was made for
    seat = models.IntegerField() # position the player's entry should be in for the grader
    code = models.TextField() # code of the submission
    score = models.FloatField(null=True, blank=True) # resulting score of the round for the team
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE) # team that made the submission
    class Meta:
        db_table = "submissions_airound"
