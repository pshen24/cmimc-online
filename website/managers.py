from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        print("creating user")
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        print("creating user")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class ScoreManager(models.Manager):
    def create_score(self, problem, competitor):
        score = self.create(problem=problem, competitor=competitor)
        if problem.exam.is_optimization:
            score.task_scores = [0]*problem.num_tasks
        return score

    def getScore(self, problem, competitor):
        score = self.filter(problem=problem, competitor=competitor).first()
        if score:
            return score
        else:
            new_score = self.create_score(problem=problem, competitor=competitor)
            return new_score

class CompetitorManager(models.Manager):
    def mathleteToCompetitor(self, exam, mathlete):
        team = mathlete.teams.filter(contest=exam.contest).first()
        if exam.is_team_exam:
            return self.get(exam=exam, team=team, mathlete=None)
        else:
            return self.get(exam=exam, team=team, mathlete=mathlete)
