from django.shortcuts import render
from django.http import HttpResponse
from website.models import Contest


def home(request):
    return render(request, 'home.html')

def contest_list(request):
    all_contests = Contest.objects.all()
    context = {
        'all_contests': all_contests
    }
    return render(request, 'contest_list.html', context)
