from django.shortcuts import render

def home(request):
    return render(request, 'general/home.html')

def info(request):
    return render(request, 'general/info.html')

def schedule(request):
    return render(request, 'general/schedule.html')

def reg_info(request):
    return render(request, 'general/reg_info.html')

def faq(request):
    return render(request, 'general/faq.html')

def resources(request):
    return render(request, 'general/resources.html')

