from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
#from website import problem_graders
from website.managers import UserManager, ScoreManager, CompetitorManager
import random
import string


class Contest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    min_team_size = models.IntegerField() # if we ever need an individual contest,
    max_team_size = models.IntegerField() # set min and max team size to 1
    reg_start_date = models.DateTimeField(help_text=_('The date that registration \
            opens, and mathletes can start forming teams'))
    reg_end_date = models.DateTimeField(help_text=_('Teams can no longer be modified \
            after this date')) 

    def __str__(self):
        return self.name

    # TODO: update for coaches
    # whether the user is registered for this contest
    def is_registered(self, user):
        if not user.is_authenticated:
            return False
        if not user.is_mathlete:
            return False
        return user.has_team(self)


class Exam(models.Model):
    contest = models.ForeignKey(Contest, related_name='exams', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_team_exam = models.BooleanField()
    show_leaderboard = models.BooleanField(help_text=_('Whether to allow contestants \
            to see the leaderboard during the exam'))
    show_own_scores = models.BooleanField(help_text=_('Whether to allow contestants \
            to see their scores during the exam')) 

    def __str__(self):
        return self.name

    @cached_property
    def _now(self):
        return timezone.now()

    @cached_property
    def ended(self):
        return self._now > self.end_time

    @cached_property
    def started(self):
        return self._now >= self.start_time

    @cached_property
    def ongoing(self):
        return self.started and not self.ended

    @cached_property
    def time_until_start(self):
        if not self.started:
            return self.start_time - self._now
        else:
            return None

    @cached_property
    def time_remaining(self):
        if not self.ended:
            return self.end_time - self._now
        else:
            return None

    # whether the user is currently doing the exam
    def is_in_exam(self, user):
        return self.ongoing and self.contest.is_registered(user)

    # whether the user has access to the leaderboard page
    def can_see_leaderboard(self, user):
        if user.is_staff:
            return True
        if not self.ended and not self.contest.is_registered(user):
            return False
        return self.show_leaderboard

    # whether the user has access to the status page
    def can_see_status(self, user):
        if user.is_staff: # they have access to the status page, but no scores are shown
            return True
        if not self.contest.is_registered(user):
            return False
        if self.ended:
            return True
        if not self.started:
            return False
        return self.show_own_scores

    # whether the user has access to the problem pages
    def can_see_problems(self, user):
        if user.is_staff:
            return True
        if self.ended:
            return True
        if not self.started:
            return False
        return self.contest.is_registered(user)


class Problem(models.Model):
    exam = models.ForeignKey(Exam, related_name='problems', on_delete=models.CASCADE)
    problem_text = models.CharField(max_length=1000)
    name = models.CharField(max_length=100, unique=True)
    grader_name = models.CharField(max_length=50) # add choices?
    grader_data = models.JSONField(null=True, blank=True, help_text=_("Data for the \
            problem's grader to use. The format depends on the type of grader"))
    problem_number = models.CharField(max_length=2, help_text=_("For most exams, \
            problems are numbered 1, 2, 3, ..., but for the optimization round, \
            they are numbered 1a, 1b, 1c, 2a, 2b, ... (each problem has multiple test cases"))
    
    # returns an instance of the grader class defined by grader_name
    @cached_property
    def grader(self):
        class_ = getattr(problem_graders, self.grader_name)
        return class_(self)

    # add max submission limit?

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['exam', 'problem_number']


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(max_length=100, help_text=_('full name'))
    alias = models.CharField(max_length=100, blank=True, help_text=_('preferred name'))

    MATHLETE = 'ML'
    STAFF = 'ST'
    COACH = 'CO'
    role_CHOICES = [
        (MATHLETE, 'Contestant'),
        (STAFF, 'CMU Student'),
        (COACH, 'Coach'),     # coaches not implemented yet
    ]
    role = models.CharField(max_length=2, choices=role_CHOICES, default=MATHLETE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.preferred_name

    @property
    def preferred_name(self):
        if self.alias:
            return self.alias
        return self.full_name

    @property
    def is_mathlete(self):
        return self.role == self.MATHLETE

    @property
    def is_coach(self):
        return self.role == self.COACH

    def has_team(self, contest):
        if self.is_staff:
            return False
        elif self.is_mathlete:
            return self.mathlete.teams.filter(contest=contest).exists()
        else:
            return self.teams.filter(contest=contest).exists()



class Mathlete(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='mathlete', \
            unique=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Mathlete: " + str(self.user)

    def get_team(self, contest):
        return self.teams.filter(contest=contest).first()



class Team(models.Model):
    contest = models.ForeignKey(Contest, related_name='teams', on_delete=models.CASCADE)
    mathletes = models.ManyToManyField(Mathlete, related_name='teams')
    is_registered = models.BooleanField(default=False, help_text=_('The members of a \
            registered team are finalized and cannot be edited'))
    coach = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, \
                              related_name='teams', on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100)
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
        name = "Team: ["
        for m in self.mathletes.all():
            name += str(m) + ", "
        name += "]"
        return name

    class Meta:
        unique_together = ['team_name', 'contest']

    def register(self):
        # TODO: check if this is during the contest registration period
        assert(not self.is_registered)
        size = self.mathletes.count()
        assert(size >= self.contest.min_team_size and size <= self.contest.max_team_size)
        for exam in self.contest.exams.all():
            if exam.is_team_exam:
                c = Competitor(exam=exam, team=self, mathlete=None)
                c.save()
            else:
                for m in self.mathletes.all():
                    c = Competitor(exam=exam, team=self, mathlete=m)
                    c.save()
        self.is_registered = True
        self.save()

    def unregister(self):
        assert(self.is_registered)
        for c in self.competitors.all():
            c.delete()
        self.is_registered = False
        self.save()

    # whether the user has access to the team info page
    def can_see_info(self, user):
        if user.is_staff:
            return True
        if user.is_mathlete:
            return user.mathlete.teams.filter(pk=self.id).exists()
        if user.is_coach:
            return self.coach == user

    @property
    def mathlete_list(self):
        if not self.mathletes.exists():
            return 'No students'
        m = [m.user.preferred_name for m in self.mathletes.all()]
        return ', '.join(m)




class Competitor(models.Model):
    exam = models.ForeignKey(Exam, related_name='competitors', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='competitors', on_delete=models.CASCADE)
    mathlete = models.ForeignKey(Mathlete, blank=True, null=True, \
            related_name='competitors', on_delete=models.CASCADE, \
            help_text=_('If the exam is an individual exam, this is the \
            corresponding mathlete. If the exam is a team exam, this is null'))
    total_score = models.IntegerField(default=True, db_index=True)

    objects = CompetitorManager()

    class Meta:
        unique_together = ['exam', 'team', 'mathlete']

    @property
    def is_team(self):
        return self.exam.is_team_exam

    def __str__(self):
        if self.is_team:
            return "Comp: " + str(self.team)
        else:
            return "Comp: " + str(self.mathlete)

    def update_total_score(self):
        self.total_score = 0
        for s in self.scores.all():
            self.total_score += s.points
        self.save()


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
    # add something for errors? (if they submit something invalid)

    def __str__(self):
        return str(self.competitor) + "'s submission to problem " + str(self.problem)

    def grade(self):
        self.problem.grader.grade(self)


class Score(models.Model):
    problem = models.ForeignKey(Problem, related_name='scores', on_delete=models.CASCADE)
    competitor = models.ForeignKey(Competitor, related_name='scores', on_delete=models.CASCADE)
    points = models.FloatField(default=0.0)
    grader_data = models.JSONField(null=True, blank=True, help_text=_("Extra data that \
            custom graders can use. The format depends on the problem's grader"))

    objects = ScoreManager()

    def __str__(self):
        return 'Score: (' + str(self.problem) + ', ' + str(self.competitor) + ') = ' \
                + str(self.points)

    class Meta:
        unique_together = ['problem', 'competitor']

class Snippet(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )

