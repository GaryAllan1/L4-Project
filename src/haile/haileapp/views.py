from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from .forms import SignUpForm, LoginForm, ChatPromptForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from .models import *
import os
import openai
from dotenv import load_dotenv
import time

def call_api(prompt):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in algorithms and data strucutres."},
            {"role": "user", "content": prompt}
        ]
    )
    response = completion.choices[0].message["content"]
    # time.sleep(10)
    # response = "this is a test response"
    return response

def index(request):
    if request.user.is_authenticated:
        context_dict = {'user': request.user}
    else:
        context_dict = {}
    return render(request, 'index.html', context=context_dict)

def study(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('signup'))
    
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest': # check if ajax
        form = ChatPromptForm(request.POST)
        if form.is_valid():
            prompt_text = form.cleaned_data['prompt_text']
            prompt_text = "limit your response to 150 words. " + prompt_text
            response = call_api(prompt_text)
            # create chat prompt in database
            haile_user = HaileUser.objects.get(user=request.user)
            ChatPrompt.objects.create(user_id=haile_user, prompt_text=prompt_text, section_from='study', ai_response=response)
            
            return JsonResponse({'response': response}, status=200)
        else:
            return JsonResponse({'errors': form.errors.as_json()}, status=400)
    else:
        form = ChatPromptForm()
        return render(request,'study.html', {'form': form})


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

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse("Invalid login details supplied.")
                
                
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
def quiz(request, question=1):
    return render(request, 'question1.html')