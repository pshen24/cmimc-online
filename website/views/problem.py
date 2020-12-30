from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from website.models import Exam, Problem, Task, Competitor, Score
from django.http import HttpResponse

@login_required
def view_problem(request, exam_id, problem_number):
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    if not exam.can_view(user):
        raise PermissionDenied("You must be registered for the contest to see \
                the problems")

    problem = get_object_or_404(Problem, exam=exam, problem_number=problem_number)

    # TODO: needs to work for coaches too (except they can't submit)
    if user.is_mathlete:
        if exam.is_optimization:
            mathlete = user.mathlete
            competitor = Competitor.objects.getCompetitor(exam, mathlete)
            score = Score.objects.getScore(problem, competitor)
            task_scores = {} # dictionary with tasks as key and scores as value
            for i in range(problem.num_tasks):
                task = Task.objects.get(problem=problem, task_number=i+1)
                pts = score.task_scores[i]
                task_scores[task] = pts
        else:
            task_scores = None
        context = {
            'problem': problem,
            'task_scores': task_scores,
            'exam': exam,
        }
        return render(request, 'exam/view_problem.html', context)


