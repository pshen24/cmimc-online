from django.db import models
from .team import Team

class Submission(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE) # game that submission was made for
    seat = models.IntegerField() # position the player's entry should be in for the grader
    code = models.TextField() # code of the submission
    score = models.FloatField() # resulting score of the round for the team
    team = models.ForeignKey(Team) # team that made the submission
    class Meta:
        db_table = "submissions_airound"

class Game(models.Model):
    """
    0 = in queue
    1 = running
    2 = graded
    """
    status = models.IntegerField(default = 0)
    history = models.JSONField() # after the game is played, gives the history output of the grader
    time = models.TimeField() # when the game should be played
    numplayers = models.IntegerField() # number of players
    contest = models.ForeignKey(Contest) # which contest to use
    worker = models.ForeignKey(Grader) # which grader was used to grade this
    class Meta:
        db_table = "games_airound"
    

class Contest(models.Model):
    code = models.TextField() # python grading code for the contest
    class Meta:
        db_table = "contests_airound"

class Grader(model.Model):
    hostname = models.TextField() # hostname of the grader
    currently = models.TextField() # current status of the grader
    class Meta:
        db_table = "graders_airound"
