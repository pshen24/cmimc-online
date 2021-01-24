from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from website.models import Exam, Problem, Score, Competitor, TaskScore, Task


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
        "scores": [round(Score.objects.get(problem=p, competitor=comp).points, 1) for p in problems],
        "total_score": round(comp.total_score, 1)
    } for comp in comps]

    context = {
        'comp_info': comp_info,
        'problems': problems,
        'exam': exam,
    }
    return render(request, 'exam/leaderboard.html', context)

@login_required
def leaderboard_problem(request, exam_id, problem_id):
    # Authentication
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    problem = get_object_or_404(Problem, pk=problem_id, exam=exam)

    comps = Competitor.objects.filter(exam=exam).order_by('-total_score')

    comp_info = []

    tasks = Task.objects.filter(problem=problem)

    for comp in comps:
        task_scores = []
        for task in tasks:
            got_task_score = False
            scores = Score.objects.filter(competitor=comp, problem = problem).order_by('-points')
            for score in scores:
                if not got_task_score:
                    try:
                        task_score = TaskScore.objects.get(task=task, score=score)
                        task_scores.append(task_score.raw_points)
                        got_task_score = True
                    except:
                        got_task_score = False

            if not got_task_score:
                task_scores.append({
                    "name": comp.name,
                    "scores": "",
                    "total_score": comp.total_score
                })

        comp_info.append({
            "name": comp.name,
            "scores": task_scores,
            "total_score": comp.total_score
        })

    context = {
        'comp_info': comp_info,
        'tasks': tasks,
        'exam': exam,
    }
    return render(request, 'exam/leaderboard_problem.html', context)
