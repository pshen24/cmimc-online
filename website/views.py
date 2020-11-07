from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from website.models import Contest, Exam, Problem, Competitor, Submission, Score, Team
from website.forms import UserCreationForm


def home(request):
    return render(request, 'home.html')


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
            team = mathlete.get_team(contest)
            return redirect('team_info', team_id=team.id)
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
    print(tuples)
    context = {
        'tuples': tuples
    }
    return render(request, 'contest_list.html', context)


@login_required
def team_info(request, team_id):
    user = request.user
    team = get_object_or_404(Team, pk=team_id)
    if not team.can_see_info(user):
        return redirect('home')

    if request.method == 'POST':
        if request.POST['submit'] == 'leaveTeam' and user.is_mathlete:
            mathlete = user.mathlete
            team.mathletes.remove(mathlete)
        elif request.POST['submit'] == 'register':
            team.register()

    context = {
        'team': team,
        'invite_link': request.build_absolute_uri(
            reverse('join_team', args=[team_id, team.invite_code])
        ),
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
        'teams': teams
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
