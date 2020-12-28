from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from website.models import Exam, Problem, Task, Competitor, Submission
from website.forms import EditorForm

@login_required
def submit(request, exam_id, problem_number, task_number=None):
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    if not exam.is_in_exam(user):
        raise PermissionDenied("You must be registered for the contest to access \
                the submission page")

    problem = get_object_or_404(Problem, exam=exam, problem_number=problem_number)
    task = Task.objects.filter(problem=problem, task_number=task_number).first()

    if request.method == 'POST':
        return make_submission(request, exam, problem, task)
    else: # request.method == 'GET'
        return show_form(request, exam, problem, task)


@login_required
def resubmit(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    problem = submission.problem
    exam = problem.exam
    task = submission.task

    if request.method == 'POST':
        return make_submission(request, exam, problem, task)
    else: # request.method == 'GET'
        text = submission.text
        return show_form(request, exam, problem, task, text)


def make_submission(request, exam, problem, task=None):
    user = request.user
    # get text
    if 'codeFile' in request.FILES:
        text = request.FILES['codeFile'].read().decode('utf-8')
    else:
        if exam.is_optimization:
            text = request.POST['codeText']
        elif exam.is_ai:
            form = EditorForm(request.POST)
            text = form['text'].value()
        else:
            return HttpResponse('Error: Only optimization and AI rounds are supported right now')
    # create and save submission
    competitor = Competitor.objects.getCompetitor(exam, user.mathlete)
    submission = Submission(
        problem=problem,
        competitor=competitor,
        text=text,
        task=task,
    )
    submission.save()
    # grade the new submission
    submission.grade()
    return redirect('all_problems', exam_id=exam.id)


def show_form(request, exam, problem, task, text=''):
    if exam.is_optimization:
        context = {
            'problem': problem,
            'task': task,
            'text': text,
        }
        return render(request, 'submit/submit_opt.html', context)
    elif exam.is_ai:
        form = EditorForm({'text': text})
        context = {
            'problem': problem,
            'form': form,
        }
        return render(request, 'submit/submit_ai.html', context)
    else:
        return HttpResponse('Error: Only optimization and AI rounds are supported right now')


