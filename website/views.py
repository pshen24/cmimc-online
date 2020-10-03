from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from website.models import Contest, Team
from website.forms import UserCreationForm


def home(request):
    return render(request, 'home.html')

def contest_list(request):
    all_contests = Contest.objects.all()
    context = {
        'all_contests': all_contests
    }
    return render(request, 'contest_list.html', context)


@login_required
def join_contest(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    assert(request.user.is_mathlete)
    mathlete = request.user.mathlete

    team = mathlete.teams.filter(contest=contest).first()
    if team:
        # this mathlete already has a team for this contest
        return redirect('team_info', team_id=team.id)
    
    context = {
        # add info here
    }
    return render(request, 'join_contest.html', context)


@login_required
def team_info(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    context = {
        # add info here
        'team': team,
    }
    return render(request, 'join_contest.html', context)


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
