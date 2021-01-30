from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from website.models import Exam, Competitor, Submission, AISubmission, AIProblem
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import json

@login_required
def match_replay(request, aisubmission_id):
    user = request.user
    aisub = get_object_or_404(AISubmission, pk=aisubmission_id)
    if not user.in_team(aisub.competitor.team):
        raise PermissionDenied("You do not have access to view this match")

    gamedata = aisub.game.history
    replay = {"seat": aisub.seat, "gamedata": gamedata}
    content = json.dumps(replay)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=replay{0}.txt'.format(aisubmission_id)
    return response

@login_required
def ai_starter_file(request, aiproblem_id):
    user = request.user
    aiprob = get_object_or_404(AIProblem, pk=aiproblem_id)
    problem = aiprob.problem
    exam = problem.exam
    if not user.can_view_exam(exam):
        raise PermissionDenied("You do not have access to this file")

    content = aiprob.starter_file
    response = HttpResponse(content, content_type='text/x-python')
    response['Content-Disposition'] = 'attachment; filename={0}_starter.py'.format(problem.short_name)
    return response


@login_required
def ai_visualizer(request, aiproblem_id):
    user = request.user
    aiprob = get_object_or_404(AIProblem, pk=aiproblem_id)
    problem = aiprob.problem
    exam = problem.exam
    if not user.can_view_exam(exam):
        raise PermissionDenied("You do not have access to this file")

    content = aiprob.visualizer
    response = HttpResponse(content, content_type='text/x-python')
    response['Content-Disposition'] = 'attachment; filename={0}_visualizer.py'.format(problem.short_name)
    return response



