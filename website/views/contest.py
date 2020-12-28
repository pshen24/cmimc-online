from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from website.models import Contest, User

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

    context = {
        'tuples': tuples,
        'emaillist': ', '.join(all_emails),
    }
    return render(request, 'contest_list.html', context)

