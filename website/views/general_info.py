from django.shortcuts import render

def home(request):
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

