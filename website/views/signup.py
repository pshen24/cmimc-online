from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from website.models import User, Mathlete
from website.forms import UserCreationForm

# User Account Signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=raw_password)
            login(request, user)
            if form.cleaned_data.get('role') == User.MATHLETE:
                mathlete = Mathlete(user=user)
                mathlete.save()
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect('contest_list')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
        'next': request.GET.get('next'),
    }
    return render(request, 'signup.html', context)

