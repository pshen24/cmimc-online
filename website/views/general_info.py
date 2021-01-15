from django.shortcuts import render
from background_task import background
import datetime

@background
def hello():
    print("Time is:" + str(datetime.datetime.now()))

@background
def start():
    print("START Time is:" + str(datetime.datetime.now()))
    hello(schedule=10, repeat=5, repeat_until=datetime.datetime.now()+datetime.timedelta(seconds=30))

def home(request):
    print("HOME Time is:" + str(datetime.datetime.now()))
    #hello(repeat=10, repeat_until=datetime.datetime.now()+datetime.timedelta(seconds=20))
    hello(schedule=10, repeat=5, repeat_until=datetime.datetime.now()+datetime.timedelta(seconds=30))
    return render(request, 'general/home.html')

def info(request):
    return render(request, 'general/info.html')

def sample_problems(request):
    return render(request, 'general/sample_problems.html')

def schedule(request):
    return render(request, 'general/schedule.html')

def reg_info(request):
    return render(request, 'general/reg_info.html')

def faq(request):
    return render(request, 'general/faq.html')

def mini_events(request):
    return render(request, 'general/mini_events.html')

def resources(request):
    return render(request, 'general/resources.html')

