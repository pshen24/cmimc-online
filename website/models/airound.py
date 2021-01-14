from django.db import models
from .team import Team
from website.models import Exam, Team
from django.shortcuts import render, get_object_or_404
from background_task import background
import datetime



class AIGame(models.Model):
    """
    0 = in queue
    1 = running
    2 = graded
    """
    status = models.IntegerField(default = 0)
    history = models.JSONField() # after the game is played, gives the history output of the grader
    time = models.TimeField() # when the game should be played
    numplayers = models.IntegerField() # number of players
    contest = models.ForeignKey(Exam, on_delete=models.CASCADE) # which exam to use
    #worker = models.ForeignKey(AIGrader) # which grader was used to grade this
    class Meta:
        db_table = "games_airound"

class AISubmission(models.Model):
    game = models.ForeignKey(AIGame, on_delete=models.CASCADE) # game that submission was made for
    seat = models.IntegerField() # position the player's entry should be in for the grader
    code = models.TextField() # code of the submission
    team = models.ForeignKey(Team, on_delete=models.CASCADE) # team that made the submission
    class Meta:
        db_table = "submissions_airound"

class AIGrader(models.Model):
    hostname = models.TextField() # hostname of the grader
    currently = models.TextField() # current status of the grader
    class Meta:
        db_table = "graders_airound"


@background(schedule=0)
def initialize_one(exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)

    #TODO make schedule, right now just puts all things at the same time

    teams = Team.objects.filter(contest=exam.contest)

    counter = 0
    curr_game = None
    for team in teams:
        if(counter==0):
            temp_game = AIGame(history=None, time=exam.start_time, numplayers=4, contest=exam)
            temp_game.save()
            curr_game = temp_game

        temp_sub = AISubmission(game=curr_game, seat = counter, code=None, team=team)
        temp_sub.save()
        counter+=1
        counter%=4

def initialize_all():
    exams = Exam.objects.all()
    for exam in exams:
        if exam.is_ai and not exam.started:
            initialize_one(exam.id, schedule=exam.start_time)