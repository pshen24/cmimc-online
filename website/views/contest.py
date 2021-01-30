from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from website.models import Contest, User, Exam, Mathlete, Team
from django.utils import timezone
from website.tasks import init_all_tasks
from website.utils import update_contest, reset_contest, regrade_games, log

@login_required
def contest_list(request):

    if request.method == 'POST':
        if 'update_contest' in request.POST:
            contest = Contest.objects.get(pk=request.POST['update_contest'])
            update_contest(contest)
        elif 'reset_contest' in request.POST:
            contest = Contest.objects.get(pk=request.POST['reset_contest'])
            reset_contest(contest)
        elif 'init_all_tasks' in request.POST:
            init_all_tasks()
        elif 'regrade_games' in request.POST:
            regrade_games()

    user = request.user
    all_contests = Contest.objects.all()
    if not user.is_tester:
        all_contests = all_contests.filter(is_private=False)     # hide private contests

    tuples = []
    for contest in all_contests:
        if user.is_mathlete:
            if user.has_team(contest):
                team = user.mathlete.get_team(contest)
                tuples.append({'contest':contest, 'has_team':True, 'team':team, 'exams': contest.exams.all(), 'canjoin': contest.started})
            else:
                tuples.append({'contest':contest, 'has_team':False, 'team':None, 'exams': contest.exams.all(), 'canjoin': False})
        else:
            tuples.append({'contest':contest, 'has_team':user.has_team(contest), 'team':None, 'exams': contest.exams.all(), 'canjoin': contest.started})
    
    # Categorize the contests in the tuples
    ongoing_contests = []
    for t in tuples:
        if t['contest'].ongoing:
            ongoing_contests.append(t)
    upcoming_contests = []
    for t in tuples:
        if not t['contest'].started:
            upcoming_contests.append(t)
    past_contests = []
    for t in tuples:
        if t['contest'].ended:
            past_contests.append(t)
    
    # Get all exams
    all_exams = Exam.objects.all()
    all_emails = []
    prog_emails = []
    small_teams = []
    member_count = [0]*10

    if user.is_staff:

        # Temporary email list (only visible to staff)
        all_users = User.objects.all()
        for user in all_users:
            all_emails.append(user.email)

        c = Contest.objects.get(pk=1) # programming contest
        teams = Team.objects.filter(contest=c)
        for team in teams:
            member_count[min(team.mathletes.all().count(), 9)] += 1
            for m in team.mathletes.all():
                prog_emails.append(m.user.email)
            if team.coach:
                prog_emails.append(team.coach.email)
            if team.mathletes.all().count() < 3:
                for m in team.mathletes.all():
                    small_teams.append(m.user.email)

    context = {
        'exams': all_exams,
        'ongoing': ongoing_contests,
        'upcoming': upcoming_contests,
        'past': past_contests,
        # staff only
        'emaillist': ', '.join(all_emails),
        'prog_emails': ', '.join(prog_emails),
        'small_teams': ', '.join(small_teams),
        'member_count': member_count,
    }
    return render(request, 'contest_list.html', context)

