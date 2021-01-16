from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from website.managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
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
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.name

    @property
    def name(self):
        if self.alias:
            return self.alias
        elif self.full_name:
            return self.full_name
        else:
            return '{0} {1}'.format(self.first_name, self.last_name)

    @property
    def short_name(self):
        if self.first_name:
            return self.first_name
        else:
            return self.name

    @property
    def is_mathlete(self):
        return self.role == self.MATHLETE

    @property
    def is_coach(self):
        return self.role == self.COACH

    def has_team(self, contest):
        if self.is_mathlete:
            return self.mathlete.teams.filter(contest=contest).exists()
        elif self.is_coach:
            return self.teams.filter(contest=contest).exists()
        else:
            return False

    # TODO: update for coaches
    # whether the user is registered for this contest
    # Do we need both is_registered and has_team?
    def is_registered(self, contest):
        if not self.is_authenticated:
            return False
        if not self.is_mathlete:
            return False
        return self.has_team(contest)

    def can_edit_team(self, team):
        if self.is_staff:
            return True
        if self.is_coach:
            if self == team.coach and not team.is_finalized:
                return True
        if self.is_mathlete:
            if team.coach == None and team in self.mathlete.teams.all() and not team.is_finalized:
                return True
        return False

    # whether the user is currently doing the exam
    # TODO: check if this is actually used
    def is_in_exam(self, exam):
        return exam.ongoing and self.is_registered(exam.contest)

    # whether the user can view the exam pages, which includes:
    # 1. all problems page
    # 2. individual problem pages
    # 3. all submissions page
    # 4. individual submission pages (only when the submission belongs to them)
    # 5. leaderboard (only when the leaderboard is meant to be public)
    # 6. problem submit pages (only permission to view the page, not to submit)
    def can_view_exam(self, exam):
        if self.is_staff:
            return True
        if exam.ended:
            return True     # anyone can view a past contest
        if exam.ongoing and self.has_team(exam.contest):
            return True     # you need to be registered for an ongoing contest
        return False

    def can_view_leaderboard(self, exam):
        if self.is_staff:
            return True
        if self.can_view(exam) and exam.show_leaderboard:
            return True
        return False

    def can_submit(self, exam):
        if self.is_mathlete:
            if exam.is_ongoing and self.is_registered(exam.contest):
                return True
        return False

    def can_view_submission(self, submission):
        if self.is_staff:
            return True
        if self.is_coach and self == submission.competitor.team.coach:
            return True
        if self.is_mathlete:
            comp = Competitor.objects.getCompetitor(self.problem.exam, self.mathlete)
            if comp == submission.competitor:
                return True
        return False

    def can_create_team(self, contest):
        if self.is_staff:
            return False
        if contest.reg_ended:
            return False
        return True

    # whether the user has access to the team info page
    def can_view_team(self, team):
        if self.is_staff:
            return True
        if self.is_mathlete and team.has_member(self):
            return True
        if self.is_coach and self == team.coach:
            return True
        return False

