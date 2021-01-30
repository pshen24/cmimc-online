from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from website.models import Exam, Competitor, Score, MiniRoundScore, Problem, AISubmission
from website.utils import miniround_sub

@login_required
def all_problems(request, exam_id):
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    if not user.can_view_exam(exam):
        raise PermissionDenied('You do not have access to this page')

    problems = exam.prob_list

    prob_score_task_rank = []
    if user.is_mathlete:
        competitor = Competitor.objects.getCompetitor(exam, user.mathlete)

        num_comps = Competitor.objects.filter(exam=exam).count()
        for problem in problems:
            score = Score.objects.get(problem=problem, competitor=competitor)
            rank = Score.objects.filter(problem=problem, points__gt=score.points).count() + 1
            g = problem.grader
            if exam.is_optimization:
                task_str = ', '.join([ts.display_raw() for ts in score.taskscores.all()])
            else:
                task_str = ''
            score_str = score.display_points
            rank_str = '{0} out of {1}'.format(str(rank), str(num_comps))
            prob_score_task_rank.append((problem, score_str, task_str, rank_str))

    context = {
        'exam': exam,
        'prob_score_task_rank': prob_score_task_rank,
    }
    return render(request, 'exam/all_problems.html', context)


@login_required
def miniround_scores(request, exam_id):
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    if not user.can_view_exam(exam) or not user.is_mathlete:
        raise PermissionDenied('You do not have access to this page')

    c = Competitor.objects.getCompetitor(exam=exam, mathlete=user.mathlete)
    problems = exam.prob_list

    # TODO: let coaches see all their teams' miniround pages via tabs at the top
    rows = []
    for m in range(exam.display_miniround, 0, -1):
        scores = []
        for p in problems:
            s = Score.objects.get(problem=p, competitor=c)
            mrs = MiniRoundScore.objects.get(score=s, miniround=m)
            scores.append(round(mrs.avg_points, 2))
        rows.append({
            "miniround": m,
            "scores": scores,
        })

    context = {
        "rows": rows,
        "exam": exam,
        "problems": problems,
    } 
    return render(request, 'exam/miniround_scores.html', context)


@login_required
def match_results(request, exam_id, problem_number):
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    if not user.can_view_exam(exam) or not user.is_mathlete:
        raise PermissionDenied('You do not have access to this page')

    problems = exam.prob_list
    p = get_object_or_404(Problem, exam=exam, problem_number=problem_number)
    c = Competitor.objects.getCompetitor(exam=exam, mathlete=user.mathlete)

    # this is slow when there are many games/submissions
    aisubs = c.aisubmissions.filter(game__aiproblem__problem=p, game__status=4).order_by('-game__miniround')

    rows = []
    for aisub in aisubs:
        g = aisub.game
        rows.append({
            "miniround": g.miniround,
            "score": round(aisub.score, 2),
            "submission": miniround_sub(aisub.competitor, p, g.miniround),
            "aisub": aisub,
        })

    context = {
        "rows": rows,
        "exam": exam,
        "problems": problems,
        "problem": p,
        "aiprob": p.aiproblem.first(),
    } 
    return render(request, 'exam/match_results.html', context)




