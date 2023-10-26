from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError

def index(request):
    if request.user.is_authenticated:
        context_dict = {'user': request.user}
    return render(request, 'index.html', context=context_dict)

def study(request):
    return render(request,'study.html')

def quiz_intro(request):
    return render(request,'quiz_intro.html')

def signup(request):
    return render(request,'signup.html')
 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                user.refresh_from_db()  
                # load the profile instance created by the signal
                user.save()
                raw_password = form.cleaned_data.get('password1')

                # login user after signing up
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)

                # redirect user to home page
                return redirect('index')
            
            except IntegrityError:
                form = SignUpForm()
                return render(request,'signup.html', {'form': form,
                                                      'error_message': 'An account with that email address already exists.'})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})