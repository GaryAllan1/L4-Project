from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from .models import HaileUser

def index(request):
    if request.user.is_authenticated:
        context_dict = {'user': request.user}
    else:
        context_dict = {}
    return render(request, 'index.html', context=context_dict)

def study(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('signup'))
    return render(request,'study.html')

def quiz_intro(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('signup'))
    return render(request,'quiz_intro.html')

 
def signup(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('profile'))

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            #try:
            user = form.save()
            user.refresh_from_db()  
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')

            HaileUser.objects.create(user=user)

            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            # redirect user to home page
            return redirect('index')
            
    #         except IntegrityError:
    #             form = SignUpForm()
    #             return render(request,'signup.html', {'form': form,
    #                                                   'error_message': 'An account with that email address already exists.'})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def profile(request):
    if request.user.is_authenticated:
        print()
        print()
        print(request)
        return render(request, 'profile.html', {'user': request.user})
    else:
        return redirect('index')
    
def user_logout(request):
    logout(request)
    return redirect('index')

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            print("**************************************************")
            print(request.POST)
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse("Invalid login details supplied.")
                
                
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})