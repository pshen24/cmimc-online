from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from website.models import Exam, Competitor, Score


@login_required
def all_problems(request, exam_id):
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    if not user.can_view_exam(exam):
        raise PermissionDenied('You do not have access to this page')
    problems = exam.problems.order_by('problem_number')

    prob_score_task_rank = []
    if user.is_mathlete:
        competitor = Competitor.objects.getCompetitor(exam, user.mathlete)

        num_comps = Competitor.objects.filter(exam=exam).count()
        for problem in problems:
            score = Score.objects.get(problem=problem, competitor=competitor)
            rank = Score.objects.filter(problem=problem, points__gt=score.points).count() + 1
            g = problem.grader
            if exam.is_optimization:
                task_str = ', '.join([g.rawToString(ts.raw_points) for ts in score.taskscores.all()])
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


