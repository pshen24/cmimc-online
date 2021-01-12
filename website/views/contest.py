from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from website.models import Contest, User, Exam, Mathlete, Team
from django.utils import timezone
from website.views.team import finalize_all_teams

@login_required
def contest_list(request):

    if request.method == 'POST':
       finalize_all_teams(request, request.POST['contest_id'])

    user = request.user
    all_contests = Contest.objects.all()
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

    # Get all exams
    all_exams = Exam.objects.all()

    # Temporary email list (only visible to staff)
    all_users = User.objects.all()
    all_emails = []
    for user in all_users:
        all_emails.append(user.email)

    c = Contest.objects.get(pk=1)
    teams = Team.objects.filter(contest=c, is_finalized=False)
    unreg_emails = []
    for team in teams:
        for m in team.mathletes.all():
            unreg_emails.append(m.user.email)
        if team.coach:
            unreg_emails.append(team.coach.email)

    context = {
        'exams': all_exams,
        'tuples': tuples,
        'emaillist': ', '.join(all_emails),
        'unreg_emails': ', '.join(unreg_emails),
    }
    return render(request, 'contest_list.html', context)

