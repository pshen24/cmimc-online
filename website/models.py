from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.conf import settings
from website import problem_graders
from website.managers import UserManager, ScoreManager


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


class Exam(models.Model):
    contest = models.ForeignKey(Contest, related_name='exams', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_team_exam = models.BooleanField()
    show_leaderboard = models.BooleanField(help_text=_('Whether to allow contestants \
            to see the leaderboard during the exam'))
    show_own_scores = models.BooleanField(help_text=_('Whether to allow contestants \
            to see the score of a submission immediately after they submit')) 

    def __str__(self):
        return self.name


class Problem(models.Model):
    exam = models.ForeignKey(Exam, related_name='problems', on_delete=models.CASCADE)
    problem_text = models.CharField(max_length=1000)
    name = models.CharField(max_length=100, unique=True)
    grader_name = models.CharField(max_length=50) # add choices?
    grader_data = models.JSONField(null=True, blank=True, help_text=_("Data for the \
            problem's grader to use. The format depends on the type of grader"))
    # add problem number?
    
    # returns an instance of the grader class defined by grader_name
    @cached_property
    def grader(self):
        class_ = getattr(problem_graders, self.grader_name)
        return class_(self)

    # add max submission limit?

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(max_length=100, help_text=_('full name'))
    alias = models.CharField(max_length=100, blank=True, help_text=_('preferred name'))

    MATHLETE = 'ML'
    STAFF = 'ST'
    role_CHOICES = [
        (MATHLETE, 'Contestant'),
        (STAFF, 'CMU Student'),
        # (COACH, 'Coach'),     # coaches not implemented yet
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


class Mathlete(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='mathlete', \
            unique=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Mathlete: " + str(self.user)


class Team(models.Model):
    contest = models.ForeignKey(Contest, related_name='teams', on_delete=models.CASCADE)
    mathletes = models.ManyToManyField(Mathlete, related_name='teams')
    is_registered = models.BooleanField(default=False, help_text=_('The members of a \
            registered team are finalized and cannot be edited'))
    team_leader = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, \
            on_delete=models.SET_NULL)
    team_name = models.CharField(max_length=100,unique=true)
    invite_code = models.IntegerField()

    def __str__(self):
        name = "Team: ["
        for m in self.mathletes.all():
            name += str(m) + ", "
        name += "]"
        return name


class Competitor(models.Model):
    exam = models.ForeignKey(Exam, related_name='competitors', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='competitors', on_delete=models.CASCADE)
    mathlete = models.ForeignKey(Mathlete, blank=True, null=True, \
            related_name='competitors', on_delete=models.CASCADE, \
            help_text=_('If the exam is an individual exam, this is the \
            corresponding mathlete. If the exam is a team exam, this is null'))
    total_score = models.IntegerField(default=True, db_index=True)

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
    text = models.TextField(help_text=_('The string that the competitor submitted. \
            Its format depends on the exam (can be an integer, source code, \
            program output, etc)'))
    submit_time = models.DateTimeField(db_index=True)
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


