from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from website.models import Contest, Exam, Problem, User, Mathlete, Competitor, Submission, Score, Team
from website.forms import UserCreationForm
from website.forms import SnippetForm
from website.models import Snippet
from django import forms

def home(request):
    return render(request, 'home.html')

def info(request):
    return render(request, 'info.html')

def schedule(request):
    return render(request, 'schedule.html')

def reg_info(request):
    return render(request, 'reg_info.html')

def faq(request):
    return render(request, 'faq.html')

def resources(request):
    return render(request, 'resources.html')

# TODO: handle error when user submits a duplicate team name
# TODO: check registration period to see if new teams can still be made
@login_required
def new_team(request, contest_id):
    user = request.user
    contest = get_object_or_404(Contest, pk=contest_id)
    if user.is_mathlete:
        mathlete = user.mathlete
        if user.has_team(contest):
            team = mathlete.get_team(contest)
            return redirect('team_info', team_id=team.id)
        elif request.method == 'GET':
            return render(request, 'new_team.html')
        else:
            team = Team.create(contest=contest, team_name=request.POST['teamName'], coach=None)
            team.save()
            team.mathletes.add(mathlete)
            return redirect('team_info', team_id=team.id)
    elif user.is_coach:
        if request.method == 'GET':
            return render(request, 'new_team.html')
        else:
            team = Team.create(contest=contest, team_name=request.POST['teamName'], coach=user)
            team.save()
            return redirect('team_info', team_id=team.id)



# TODO: prevent joining after team is registered
@login_required
def join_team(request, team_id, invite_code):
    user = request.user
    team = get_object_or_404(Team, pk=team_id, invite_code=invite_code)
    contest = team.contest
    if user.is_mathlete:
        mathlete = user.mathlete
        if user.has_team(contest):
            real_team = mathlete.get_team(contest)
            return redirect('team_info', team_id=real_team.id)
        elif team.is_registered:
            return redirect('contest_list')
        else:
            team.mathletes.add(mathlete)
            return redirect('team_info', team_id=team.id)


@login_required
def contest_list(request):
    user = request.user
    all_contests = Contest.objects.all()
    tuples = []
    for contest in all_contests:
        if user.is_mathlete:
            if user.has_team(contest):
                team = user.mathlete.get_team(contest)
                tuples.append({'contest':contest, 'has_team':True, 'team':team})
            else:
                tuples.append({'contest':contest, 'has_team':False, 'team':None})
        else:
            tuples.append({'contest':contest, 'has_team':user.has_team(contest), 'team':None})
    context = {
        'tuples': tuples
    }
    return render(request, 'contest_list.html', context)


@login_required
def team_info(request, team_id):
    user = request.user
    team = get_object_or_404(Team, pk=team_id)
    if not team.can_see_info(user):
        return redirect('contest_list')

    if request.method == 'POST':
        if request.POST['submit'] == 'leaveTeam' and user.is_mathlete and not team.is_registered:
            mathlete = user.mathlete
            team.mathletes.remove(mathlete)
            return redirect('contest_list')
        elif request.POST['submit'] == 'deleteTeam' and (user.is_coach or user.is_staff):
            team.delete()
            return redirect('contest_list')
        elif request.POST['submit'] == 'register':
            team.register()

    context = {
        'team': team,
        'invite_link': request.build_absolute_uri(
            reverse('join_team', args=[team_id, team.invite_code])
        ),
        'too_large': len(team.mathletes.all()) > team.contest.max_team_size,
        'reg_permission': user != team.coach,
    }
    return render(request, 'team.html', context)


@login_required
def coach_teams(request, contest_id):
    user = request.user
    contest = get_object_or_404(Contest, pk=contest_id)
    if not user.is_coach:
        return redirect('home')

    teams = Team.objects.filter(contest=contest, coach=user)
    context = {
        'teams': teams,
        'contest': contest,
    }
    return render(request, 'coach_teams.html', context)


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
        """ if 'codeFile' in request.FILES:
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
        return redirect('exam_status', exam_id=exam_id) """

        # # Included django_ace editor
        # form = SnippetForm(request.POST)
        # if (form.is_valid()):
        #     form.save()
        #     text = Snippet.objects.all()[0].text
        #     print(text)
        #     Snippet.objects.all().delete()  # delete this line to record past snippets
        # else:
        #     text = request.FILES['codeFile'].read().decode('utf-8')
        # competitor = Competitor.objects.mathleteToCompetitor(exam, user.mathlete)
        # submission = Submission(
        #     problem=problem,
        #     competitor=competitor,
        #     text=text
        # )
        # submission.save()
        # submission.grade()
        # return redirect('exam_status', exam_id=exam_id)

        # Upload to Editor instead of submitting file
        form = SnippetForm(request.POST)
        if (form.is_valid()):
            form.save()
            text = Snippet.objects.all()[0].text
            print(text)
            Snippet.objects.all().delete()  # delete this line to record past snippets
            competitor = Competitor.objects.mathleteToCompetitor(exam, user.mathlete)
            submission = Submission(
                problem=problem,
                competitor=competitor,
                text=text
            )
            submission.save()
            submission.grade()
            return redirect('exam_status', exam_id=exam_id)
        else:
            text = request.FILES['codeFile'].read().decode('utf-8')
            competitor = Competitor.objects.mathleteToCompetitor(exam, user.mathlete)
            submission = Submission(
                problem=problem,
                competitor=competitor,
                text=text
            )
            submission.save()
            return redirect('submit_written', exam_id, problem_number, submission.pk, True)
    else: # request.method == 'GET'
        form = SnippetForm()
        context = {
            'problem': problem,
            'form': form,
            'snippets': Snippet.objects.all()
        }
        return render(request, 'submit.html', context)

@login_required
def submit_written(request, exam_id, problem_number, submit_id, is_file_upload):
    user = request.user
    exam = get_object_or_404(Exam, pk=exam_id)
    if not exam.is_in_exam(user):
        raise PermissionDenied("You must be registered for the contest to access \
                the submission page")

    problem = get_object_or_404(Problem, exam=exam, problem_number=problem_number)
    if request.method == 'POST':
        # Form with default value
        form = SnippetForm(request.POST)
        if (form.is_valid()):
            form.save()
            text = Snippet.objects.all()[0].text
            print(text)
            Snippet.objects.all().delete()  # delete this line to record past snippets
            competitor = Competitor.objects.mathleteToCompetitor(exam, user.mathlete)
            submission = Submission(
                problem=problem,
                competitor=competitor,
                text=text
            )
            submission.save()
            submission.grade()
            return redirect('exam_status', exam_id=exam_id)
        else:
            text = request.FILES['codeFile'].read().decode('utf-8')
            competitor = Competitor.objects.mathleteToCompetitor(exam, user.mathlete)
            submission = Submission(
                problem=problem,
                competitor=competitor,
                text=text
            )
            submission.save()
            return redirect('submit_written', exam_id, problem_number, submission.pk, True)
    else: # request.method == 'GET'
        submission = get_object_or_404(Submission, pk=submit_id)
        data = {'text': submission.text}
        form = SnippetForm(data)
        if (is_file_upload):
            Submission.objects.get(pk=submit_id).delete()
        context = {
            'problem': problem,
            'form': form,
            'snippets': Snippet.objects.all()
        }
        return render(request, 'submit_written.html', context)


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
            print(form.cleaned_data)
            if form.cleaned_data.get('role') == User.MATHLETE:
                mathlete = Mathlete(user=user)
                mathlete.save()
            return redirect('contest_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
