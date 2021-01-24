from django.db import models
from .contest import Contest
from django.utils.functional import cached_property
from django.utils import timezone

class Exam(models.Model):
    contest = models.ForeignKey(Contest, related_name='exams', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    miniround_time = models.DurationField(null=True, blank=True)

    is_team_exam = models.BooleanField()
    
    OPTIMIZATION = 'OPT'
    AI = 'AI'
    MATH = 'MATH'
    POWER = 'POW'
    TYPE_CHOICES = [
        (OPTIMIZATION, 'Optimization'),
        (AI, 'AI'),
        (MATH, 'Math (short answer)'),
        (POWER, 'Power (proof)'),
    ]
    exam_type = models.CharField(max_length=4, choices=TYPE_CHOICES, default=OPTIMIZATION)

    def __str__(self):
        return self.name

    @cached_property
    def is_optimization(self):
        return self.exam_type == self.OPTIMIZATION

    @cached_property
    def is_ai(self):
        return self.exam_type == self.AI

    # whether to allow contestants to see the leaderboard during the exam
    @cached_property
    def show_leaderboard(self):
        if self.exam_type == self.OPTIMIZATION:
            return True
        if self.exam_type == self.AI:
            return True
        if self.exam_type == self.MATH:
            return False
        if self.exam_type == self.POWER:
            return False

    # whether to allow contestants to see their submission scores during the exam
    @cached_property
    def show_own_scores(self):
        if self.exam_type == self.OPTIMIZATION:
            return True
        if self.exam_type == self.AI:
            return True
        if self.exam_type == self.MATH:
            return False
        if self.exam_type == self.POWER:
            return False
        
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
    def time_until_start_days(self):
        if not self.started:
            return (self.start_time - self._now).days
        else:
            return None

    @cached_property
    def time_until_start_hours(self):
        if not self.started:
            return (int)((self.start_time - self._now).seconds/60/60)
        else:
            return None

    @cached_property
    def time_until_start_minutes(self):
        if not self.started:
            return (int)((self.start_time - self._now).seconds / 60)
        else:
            return None

    @cached_property
    def time_until_start_seconds(self):
        if not self.started:
            return (self.start_time - self._now).seconds
        else:
            return None

    @cached_property
    def time_remaining_days(self):
        if not self.ended:
            return (self.end_time - self._now).days
        else:
            return None

    @cached_property
    def time_remaining_hours(self):
        if not self.ended:
            return (int)((self.end_time - self._now).seconds/60/60)
        else:
            return None

    @cached_property
    def time_remaining_minutes(self):
        if not self.ended:
            return (int)((self.end_time - self._now).seconds / 60)%60
        else:
            return 0

    # number of seconds remaining in exam
    @cached_property
    def time_remaining(self):
        return max((self.end_time - self._now).total_seconds(), 0)

    def time_remaining_seconds(self):
        if not self.ended:
            return (self.end_time - self._now).seconds%60
        else:
            return None

