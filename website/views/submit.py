from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from website.models import Exam, Problem, Task, Competitor, Submission

@login_required
def submit(request, exam_id, problem_number, task_number=None):
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    if not exam.is_in_exam(user):
        raise PermissionDenied("You must be registered for the contest to access \
                the submission page")

    problem = get_object_or_404(Problem, exam=exam, problem_number=problem_number)

    if request.method == 'POST':
        if 'codeFile' in request.FILES:
            text = request.FILES['codeFile'].read().decode('utf-8')
        else:
            text = request.POST['codeText']
        competitor = Competitor.objects.getCompetitor(exam, user.mathlete)
        if exam.is_optimization:
            task = Task.objects.get(problem=problem, task_number=task_number)
        else:
            task = None
        submission = Submission(
            problem=problem,
            competitor=competitor,
            text=text,
            task=task,
        )
        submission.save()
        submission.grade()
        return redirect('all_problems', exam_id=exam_id)
    else: # request.method == 'GET'
        if exam.is_optimization:
            task = Task.objects.get(problem=problem, task_number=task_number)
            return submit_opt(request, exam, problem, task)
        elif exam.is_ai:
            return submit_ai(request, exam, problem)
        else:
            return HttpResponse('Error: Only optimization and AI rounds are supported right now')


def submit_opt(request, exam, problem, task, text=None):
    print('submit_opt, text=', text)
    context = {
        'problem': problem,
        'task': task,
        'text': text,
    }
    return render(request, 'submit/submit_opt.html', context)


def submit_ai(request, exam, problem, text=None):
    context = {
        'problem': problem,
        'text': text, # TODO: if text is not None, insert it into the IDE
    }
    return render(request, 'submit/submit_ai.html', context)


@login_required
def resubmit(request, submission_id):
    # TODO: handle POST request
    submission = get_object_or_404(Submission, pk=submission_id)
    problem = submission.problem
    exam = problem.exam
    task = submission.task
    text = submission.text
    if exam.is_optimization:
        return submit_opt(request, exam, problem, task, text)
    elif exam.is_ai:
        return submit_ai(request, exam, problem, text)
    else:
        return HttpResponse('Error: Only optimization and AI rounds are supported right now')

