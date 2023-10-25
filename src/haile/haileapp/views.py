from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse

def index(request):
    return render(request, 'index.html')

def study(request):
    return render(request,'study.html')

def quiz_intro(request):
    return render(request,'quiz_intro.html')

def signup(request):
    return render(request,'signup.html')