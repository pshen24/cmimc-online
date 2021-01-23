from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from website.models import Contest, User, Exam, Mathlete, Team
from django.utils import timezone

@login_required
def contest_list(request):

    if request.method == 'POST':
       contest = Contest.objects.get(pk=request.POST['contest_id'])
       contest.finalize_all_teams()

    user = request.user
    all_contests = Contest.objects.all()
    if not user.is_tester:
        all_contests = all_contests.filter(is_private=False)     # hide private contests

    tuples = []
    for contest in all_contests:
        if user.is_mathlete:
            if user.has_team(contest):
                team = user.mathlete.get_team(contest)
                tuples.append({'contest':contest, 'has_team':True, 'team':team, 'exams': contest.exams.all()})
            else:
                tuples.append({'contest':contest, 'has_team':False, 'team':None, 'exams': contest.exams.all()})
        else:
            tuples.append({'contest':contest, 'has_team':user.has_team(contest), 'team':None, 'exams': contest.exams.all()})
    
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

    # Temporary email list (only visible to staff)
    all_users = User.objects.all()
    all_emails = []
    for user in all_users:
        all_emails.append(user.email)

    c = Contest.objects.get(pk=1) # programming contest
    teams = Team.objects.filter(contest=c, is_finalized=True)
    member_count = [0]*10
    prog_emails = []
    for team in teams:
        member_count[min(team.mathletes.all().count(), 9)] += 1
        for m in team.mathletes.all():
            prog_emails.append(m.user.email)
        if team.coach:
            prog_emails.append(team.coach.email)

    teams = Team.objects.filter(contest=c, is_finalized=False)
    unreg_emails = []
    for team in teams:
        for m in team.mathletes.all():
            unreg_emails.append(m.user.email)
        if team.coach:
            unreg_emails.append(team.coach.email)

    context = {
        'exams': all_exams,
        'emaillist': ', '.join(all_emails),
        'unreg_emails': ', '.join(unreg_emails),
        'prog_emails': ', '.join(prog_emails),
        'ongoing': ongoing_contests,
        'upcoming': upcoming_contests,
        'past': past_contests,
        'member_count': member_count,
    }
    return render(request, 'contest_list.html', context)

