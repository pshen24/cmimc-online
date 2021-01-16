from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from website.models import Exam, Problem, Score, Competitor

@login_required
def leaderboard(request, exam_id):
    # Authentication
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    if not user.can_view_leaderboard(exam):
        raise PermissionDenied("You do not have permission to view the "
                               "leaderboard for this exam")
    problems = Problem.objects.filter(exam=exam)

    comps = Competitor.objects.filter(exam=exam).order_by('-total_score')

    comp_info = [{
        "name": comp.name,
        "scores": [Score.objects.get(problem=p, competitor=comp).points for p in problems],
        "total_score": comp.total_score
    } for comp in comps]

    context = {
        'comp_info': comp_info,
        'problems': problems,
        'exam': exam,
    }
    return render(request, 'exam/leaderboard.html', context)
