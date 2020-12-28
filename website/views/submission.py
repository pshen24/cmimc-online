from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from website.models import Exam, Competitor, Submission

@login_required
def all_submissions(request, exam_id):
    user = request.user

    exam = get_object_or_404(Exam, pk=exam_id)

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

    context = {
        'submission': submission
    }
    return render(request, 'submission/view_submission.html', context)

