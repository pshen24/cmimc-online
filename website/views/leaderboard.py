from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from website.models import Exam, Problem, Score, Competitor, TaskScore, Task, MiniRoundTotal, MiniRoundScore
from website.utils import log



def ai_leaderboard(request, exam):
    user = request.user
    problems = exam.prob_list
    m = exam.display_miniround
    mrts = MiniRoundTotal.objects.filter(competitor__exam=exam, miniround=m).order_by('-total_score')

    rows = []
    for mrt in mrts:
        c = mrt.competitor
        scores = []
        for p in problems:
            s = Score.objects.get(problem=p, competitor=c)
            mrs = MiniRoundScore.objects.get(score=s, miniround=m)
            scores.append(f'{mrs.weighted_avg:.2f}')

        rows.append({
            "name": c.name,
            "scores": scores,
            "total_score": f'{mrt.total_score:.2f}',
            "rank": mrts.filter(total_score__gt=mrt.total_score).count() + 1,
            "highlight": user.in_team(c.team),
        })

    context = {
        'rows': rows,
        'problems': problems,
        'exam': exam,
    }
    return render(request, 'exam/ai_leaderboard.html', context)




@login_required
def leaderboard(request, exam_id):
    # Authentication
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    log(user=str(user), exam=exam_id, end=exam.ended, can_view=user.can_view_exam(exam), cvl=user.can_view_leaderboard(exam))
    if not user.can_view_leaderboard(exam):
        raise PermissionDenied("You do not have permission to view the "
                               "leaderboard for this exam")

    if exam.is_ai:
        return ai_leaderboard(request, exam)

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
            "rank": comps.filter(total_score__gt=comp.total_score).count() + 1,
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
