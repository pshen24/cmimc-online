from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from website.models import Contest, User, Exam
from django.utils import timezone

@login_required
def contest_list(request):
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

    context = {
        'exams': all_exams,
        'ongoing': ongoing_contests,
        'upcoming': upcoming_contests,
        'past': past_contests,
    }
    return render(request, 'contest_list.html', context)

