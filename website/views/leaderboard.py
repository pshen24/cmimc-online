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

    problems = exam.prob_list
    comps = exam.competitors.order_by('-total_score')

    rows = []
    for comp in comps:
        scores = []
        for p in problems:
            score = Score.objects.get(problem=p, competitor=comp)
            scores.append(score.display_points)
        rows.append({
            "name": comp.name,
            "scores": scores,
            "total_score": comp.display_score,
            "rank": len(rows)+1,
            "highlight": user.in_team(comp.team),
        })

    context = {
        'rows': rows,
        'problems': problems,
        'exam': exam,
    }
    return render(request, 'exam/leaderboard.html', context)

@login_required
def problem_leaderboard(request, exam_id, problem_number):
    # Authentication
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    problem = get_object_or_404(Problem, exam=exam, problem_number=problem_number)

    tasks = problem.tasks.order_by('task_number')
    scores = problem.scores.order_by('-points')

    rows = []
    for score in scores:
        task_scores = []
        for task in tasks:
            ts = TaskScore.objects.get(task=task, score=score)
            task_scores.append(ts.display_raw(default=''))

        rows.append({
            "name": score.competitor.name,
            "scores": task_scores,
            "prob_score": score.display_points,
            "highlight": user.in_team(score.competitor.team),
        })

    context = {
        'rows': rows,
        'problem': problem,
        'tasks': tasks,
        'exam': exam,
        'problems': exam.problems.order_by('problem_number'),
    }
    return render(request, 'exam/problem_leaderboard.html', context)
