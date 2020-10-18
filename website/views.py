from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from website.models import Contest, Problem, Competitor, Exam, Submission, Score
from website.forms import UserCreationForm
#from tika import parser


def home(request):
    return render(request, 'home.html')

def general_info(request):
    return render(request, 'general_info.html')

def contest_list(request):
    all_contests = Contest.objects.all()
    context = {
        'all_contests': all_contests
    }
    return render(request, 'contest_list.html', context)


@login_required
def problem_info(request, exam_id, problem_number):
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    if not exam.can_see_problems(user):
        raise PermissionDenied("You must be registered for the contest to access \
                the submission page")

    problem = get_object_or_404(Problem, exam=exam, problem_number=problem_number)
    try:
        get_object_or_404(Problem, exam=exam, problem_number=str(int(problem_number) + 1))
        next_problem_number = str(int(problem_number)+1)
    except:
        next_problem_number = None

    context = {
        'problem': problem,
        'next_problem_number': next_problem_number,
    }
    return render(request, 'problem_info.html', context)


@login_required
def submit(request, exam_id, problem_number):
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    if not exam.is_in_exam(user):
        raise PermissionDenied("You must be registered for the contest to access \
                the submission page")

    problem = get_object_or_404(Problem, exam=exam, problem_number=problem_number)
    if request.method == 'POST':
        # TODO: Make sure that exactly one of the two inputs is submitted
        # Need a javascript event listener for when the form gets submitted
        if 'codeFile' in request.FILES:
            text = request.FILES['codeFile'].read().decode('utf-8')
        else:
            text = request.POST['codeText']
        competitor = Competitor.objects.mathleteToCompetitor(exam, user.mathlete)
        submission = Submission(
            problem=problem,
            competitor=competitor,
            text=text
        )
        submission.save()
        submission.grade()
        return redirect('exam_status', exam_id=exam_id)
    else: # request.method == 'GET'
        context = {
            'problem': problem,
        }
        return render(request, 'submit.html', context)

@login_required
def exam_status(request, exam_id):
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    if not exam.can_see_status(user):
        raise PermissionDenied('You do not have access to this page')
    problems = exam.problems.order_by('problem_number')
    if user.is_mathlete:
        competitor = Competitor.objects.mathleteToCompetitor(exam, user.mathlete)
        scores = []
        for problem in problems:
            scores.append(Score.objects.getScore(problem, competitor))
    else:
        scores = []
        for problem in problems:
            scores.append(None)

    context = {
        'exam': exam,
        'all_problems_scores': zip(problems, scores),
    }
    return render(request, 'exam_status.html', context)

# User Account Signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
