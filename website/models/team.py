from django.db import models
from .contest import Contest
from .mathlete import Mathlete
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import random

class Team(models.Model):
    contest = models.ForeignKey(Contest, related_name='teams', on_delete=models.CASCADE)
    mathletes = models.ManyToManyField(Mathlete, related_name='teams')
    is_finalized = models.BooleanField(default=False, help_text=_('The members of a \
            registered team are finalized and cannot be edited'))
    coach = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, \
                              related_name='teams', on_delete=models.SET_NULL)
    team_name = models.CharField(max_length=40)
    MIN_CODE = 100000
    MAX_CODE = 999999
    invite_code = models.CharField(unique=True, max_length=15)

    @classmethod
    def create(cls, contest, team_name, coach):
        invite_code = Team.generate_code()
        return cls(contest=contest,team_name=team_name,invite_code=invite_code,coach=coach)

    @staticmethod
    def generate_code():
        digits = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        code = ''.join(random.choice(digits) for _ in range(15))
        while Team.objects.filter(invite_code=code).exists():
            code = ''.join(random.choice(digits) for _ in range(15))
        return code

    def __str__(self):
        return '{0} ({1})'.format(self.team_name, self.mathlete_list)

    class Meta:
        unique_together = ['team_name', 'contest']

    def register(self):
        from .competitor import Competitor
        size = self.mathletes.count()
        if size < self.contest.min_team_size or size > self.contest.max_team_size:
            return
        for exam in self.contest.exams.all():
            if exam.is_team_exam:
                c = Competitor.objects.filter(exam=exam, team=self, mathlete=None).first()
                if c is None:
                    c = Competitor(exam=exam, team=self, mathlete=None)
                    c.save()
                c.init_scores(exam)
            else:
                for m in self.mathletes.all():
                    c = Competitor.objects.filter(exam=exam, team=self, mathlete=m).first()
                    if c is None:
                        c = Competitor(exam=exam, team=self, mathlete=m)
                        c.save()
                    c.init_scores(exam)

        self.is_finalized = True
        self.save()

    def unregister(self):
        for c in self.competitors.all():
            c.delete()
        self.is_finalized = False
        self.save()

    def has_member(self, user):
        return user.is_mathlete and user.mathlete.teams.filter(pk=self.id).exists()

    @property
    def mathlete_list(self):
        if not self.mathletes.exists():
            return 'No students'
        return ', '.join([m.user.name for m in self.mathletes.all()])


