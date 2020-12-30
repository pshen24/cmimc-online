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
    if user.is_mathlete:
        competitor = Competitor.objects.getCompetitor(exam, user.mathlete)

        scores = []
        task_scores = []

        # Calculates the number of people with higher score + 1
        ranks = []
        total_nums = []

        for problem in problems:
            curr_score = Score.objects.getScore(problem, competitor)
            scores.append(curr_score)

            all_scores = Score.objects.filter(problem=problem)
            problem_rank = 1
            for score in all_scores:
                if score.points > curr_score.points and score.problem_id == curr_score.problem_id:
                    problem_rank+=1

            if exam.is_optimization:
                temp = []
                for i in range(len(curr_score.task_scores)):
                    temp.append(curr_score.task_scores[i])
                task_scores.append(temp)
            else:
                task_scores.append(None)

            ranks.append(problem_rank)
            total_nums.append(len(all_scores))

    else:
        scores = []
        task_scores = []
        ranks = []
        total_nums = []
        for problem in problems:
            scores.append(None)
            task_scores.append(None)
            ranks.append(None)
            total_nums.append(None)


    context = {
        'exam': exam,
        'all_problems_scores_ranks': zip(problems, scores, task_scores,ranks, total_nums),
    }
    return render(request, 'exam/all_problems.html', context)


