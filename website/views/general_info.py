from django.shortcuts import render
from background_task import background
import datetime

def home(request):
    return render(request, 'general/home.html')

def math_info(request):
    return render(request, 'general/math_info.html')

def math_sample_problems(request):
    return render(request, 'general/math_sample_problems.html')

def math_schedule(request):
    return render(request, 'general/math_schedule.html')

def prog_info(request):
    return render(request, 'general/prog_info.html')

def prog_sample_problems(request):
    return render(request, 'general/prog_sample_problems.html')

def prog_schedule(request):
    return render(request, 'general/prog_schedule.html')

def reg_info(request):
    return render(request, 'general/reg_info.html')

def faq(request):
    return render(request, 'general/faq.html')

def mini_events(request):
    return render(request, 'general/mini_events.html')

def resources(request):
    return render(request, 'general/resources.html')

def updates(request):
    return render(request, 'general/updates.html')
