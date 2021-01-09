from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from website.models import Exam, Competitor, Score


@login_required
def all_problems(request, exam_id):
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    if not exam.can_view(user):
        raise PermissionDenied('You do not have access to this page')
    problems = exam.problems.order_by('problem_number')

    prob_score_rank = []
    if user.is_mathlete:
        competitor = Competitor.objects.getCompetitor(exam, user.mathlete)

        num_comps = Competitor.objects.filter(exam=exam).count()
        for problem in problems:
            score = Score.objects.getScore(problem, competitor)
            rank = Score.objects.filter(problem=problem, points__gt=score.points).count() + 1
            if exam.is_optimization:
                task_scores = ' + '.join(map(str, score.task_scores))
                score_str = '{0} ({1})'.format(str(score.points), task_scores)
            else:
                score_str = str(score.points)
            rank_str = '{0} out of {1}'.format(str(rank), str(num_comps))
            prob_score_rank.append((problem, score_str, rank_str))

    context = {
        'exam': exam,
        'prob_score_rank': prob_score_rank,
    }
    return render(request, 'exam/all_problems.html', context)


