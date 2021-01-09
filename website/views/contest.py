from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from website.models import Contest, User, Mathlete, Team

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

    # Temporary email list (only visible to staff)
    all_users = User.objects.all()
    all_emails = []
    for user in all_users:
        all_emails.append(user.email)

    c = Contest.objects.get(pk=1)
    teams = Team.objects.filter(contest=c, is_registered=False)
    unreg_emails = []
    for team in teams:
        for m in team.mathletes.all():
            unreg_emails.append(m.user.email)

    context = {
        'tuples': tuples,
        'emaillist': ', '.join(all_emails),
        'unreg_emails': ', '.join(unreg_emails),
    }
    return render(request, 'contest_list.html', context)

