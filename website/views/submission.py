from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from website.models import Exam, Competitor, Submission
from website.forms import ViewOnlyEditorForm
from django.core.exceptions import PermissionDenied


@login_required
def all_submissions(request, exam_id):
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    if not user.can_view_exam(exam):
        raise PermissionDenied("You do not have access to view these submissions")

    submissions = []
    if user.is_mathlete:
        competitor = Competitor.objects.getCompetitor(exam, user.mathlete)
        submissions = Submission.objects.filter(competitor=competitor).order_by('-submit_time')

    context = {
        'exam': exam,
        'submissions': submissions,
    }
    return render(request, 'submission/all_submissions.html', context)

@login_required
def view_submission(request, submission_id):
    user = request.user
    submission = get_object_or_404(Submission, pk=submission_id)
    if not user.can_view_submission(submission):
        raise PermissionDenied("You do not have access to this submission")
    exam = submission.problem.exam

    if exam.is_optimization:
        context = {
            'submission': submission,
            'exam': exam,
        }
        return render(request, 'submission/view_submission_opt.html', context)
    elif exam.is_ai:
        form = ViewOnlyEditorForm({'text': submission.text})
        context = {
            'submission': submission, 
            'form': form,
            'exam': exam,
        }
        return render(request, 'submission/view_submission_ai.html', context)
    else:
        return HttpResponse('Error: Only optimization and AI rounds are supported right now')


