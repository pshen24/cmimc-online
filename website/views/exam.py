from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from website.models import Exam, Competitor, Score

@login_required
def all_problems(request, exam_id):
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    if not exam.can_see_problems(user):
        raise PermissionDenied('You do not have access to this page')
    problems = exam.problems.order_by('problem_number')
    if user.is_mathlete:
        competitor = Competitor.objects.getCompetitor(exam, user.mathlete)
        scores = []
        for problem in problems:
            scores.append(Score.objects.getScore(problem, competitor))
    else:
        scores = []
        for problem in problems:
            scores.append(None)

    context = {
        'exam': exam,
        'all_problems_scores': zip(problems, scores),
    }
    return render(request, 'exam/all_problems.html', context)


