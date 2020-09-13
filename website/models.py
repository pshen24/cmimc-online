from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from website import problem_graders
import importlib

class Contest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    min_team_size = models.IntegerField() # if we ever need an individual contest,
    max_team_size = models.IntegerField() # set min and max team size to 1
    reg_start_date = models.DateTimeField(help_text=_('The date that registration opens, and mathletes can start forming teams'))
    reg_end_date = models.DateTimeField(help_text=_('Teams can no longer be modified after this date')) 


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Mathlete(models.Model):
    user = models.OneToOneField(User, related_name='mathlete', on_delete=models.CASCADE)


class Team(models.Model):
    contest = models.ForeignKey(Contest, related_name='teams', on_delete=models.CASCADE)
    members = models.ManyToManyField(Mathlete, related_name='teams')


class Exam(models.Model):
    contest = models.ForeignKey(Contest, related_name='exams', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_team_exam = models.BooleanField()
    show_leaderboard = models.BooleanField(help_text=_('Whether to allow contestants to see the leaderboard during the exam'))
    show_grading_score = models.BooleanField(help_text=_('Whether to allow contestants to see the score of a submission immediately after they submit')) 


class Competitor(models.Model):
    exam = models.ForeignKey(Exam, related_name='competitors', on_delete=models.CASCADE)
    team = models.OneToOneField(Team, related_name='competitor', on_delete=models.CASCADE)
    mathlete = models.ForeignKey(Mathlete, blank=True, null=True, related_name='competitors', on_delete=models.CASCADE, help_text=_('If the exam is an individual exam, this is corresponding mathlete. If the exam is a team exam, this is null'))


class Problem(models.Model):
    exam = models.ForeignKey(Exam, related_name='problems', on_delete=models.CASCADE)
    grader_name = models.CharField(max_length=50) # add choices?

    # returns an instance of the grader class defined by grader_name
    # I'm not sure if this is the best way to do it
    def grader_class(self):
        module = importlib.import_module('problem_graders' + self.grader_name)
        class_ = getattr(module, self.grader_name)
        return class_()

    # add max submissions?


class Submission(models.Model):
    problem = models.ForeignKey(Problem, related_name='submissions', on_delete=models.CASCADE)
    competitor = models.ForeignKey(Competitor, related_name='submissions', on_delete=models.CASCADE)
    text = models.TextField(help_text=_('The string that the competitor submitted. Its format depends on the exam (can be an integer, source code, program output, etc)'))
    submit_time = models.DateTimeField()
    points = models.FloatField()
    # add something for errors? (if they submit something invalid)


