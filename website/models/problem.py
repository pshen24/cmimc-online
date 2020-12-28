from django.db import models
from .exam import Exam
from ckeditor.fields import RichTextField
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils.functional import cached_property

class Problem(models.Model):
    exam = models.ForeignKey(Exam, related_name='problems', on_delete=models.CASCADE)
    problem_text = RichTextField()
    name = models.CharField(max_length=100, unique=True,
            help_text=_('The problem title that contestants see'))
    short_name = models.CharField(max_length=100, unique=True,
            help_text=_('Should be lowercase letters or numbers, no spaces'))
    grader_name = models.CharField(max_length=50) # add choices?
    grader_data = models.JSONField(null=True, blank=True, help_text=_("Data for the \
            problem's grader to use. The format depends on the type of grader"))
    problem_number = models.IntegerField(validators=[MinValueValidator(1)])
    num_tasks = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)]) # only for optimization
    pdf_link = models.CharField(max_length=1000, null=True, blank=True)
    
    # returns an instance of the grader class defined by grader_name
    @cached_property
    def grader(self):
        from website import problem_graders
        class_ = getattr(problem_graders, self.grader_name)
        return class_(self)

    # add max submission limit?

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['exam', 'problem_number']

