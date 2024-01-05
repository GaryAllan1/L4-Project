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
from django.db.models import F
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

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
        
        if request.POST.get('chat') == 'true':

            form = ChatPromptForm(request.POST)
            if form.is_valid():
                prompt_text = form.cleaned_data['prompt_text']
                prompt_text = "Be as concise as possible. " + prompt_text
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
    
def quiz(request, question):

    question_dict = {1: [1, 'MultipleChoice'], 2: [2, 'MultipleChoice'], 3: [3, 'MultipleChoice'],
                     4: [1, 'ExtendedAnswer'], 5: [2, 'ExtendedAnswer'], 6: [3, 'ExtendedAnswer']}
    

    question_type_number, question_type = question_dict[int(question)]
    question_object = get_question(question_type_number, question_type)
    if question_type == 'MultipleChoice':
        if request.method == 'POST':
            print(request.POST)
            if request.POST.get('chat') == 'true':
                # chat-bot functionality here
                form = ChatPromptForm(request.POST)
                if form.is_valid():
                    prompt_text = form.cleaned_data['prompt_text']
                    prompt_text = "Be as concise as possible. " + prompt_text
                    response = call_api(prompt_text)
                    # create chat prompt in database
                    haile_user = HaileUser.objects.get(user=request.user)
                    if request.POST.get('review') == 'true':
                        ChatPrompt.objects.create(user_id=haile_user, prompt_text=prompt_text, section_from='multiple_choice (review)', ai_response=response)
                    else:
                        ChatPrompt.objects.create(user_id=haile_user, prompt_text=prompt_text, section_from='multiple_choice (quiz)', ai_response=response)
                    
                    return JsonResponse({'response': response}, status=200)
                else:
                    return JsonResponse({'errors': form.errors.as_json()}, status=400)

            # handle the checking for correctness here
            user_answer = int(request.POST.get('selected_choice_index'))

            user = request.user
            haile_user = HaileUser.objects.filter(user=user)[0]
            if question_object.correct_choice == user_answer:
                is_correct = True   
            else:
                is_correct = False

            response, created = MultipleChoiceResponse.objects.get_or_create(
                user=haile_user,
                question=question_object,
                defaults={'is_correct': is_correct, 'selected_choice': user_answer}
            )

            if not created:
                # Update the existing record
                response.is_correct = is_correct
                response.selected_choice = user_answer
                response.save()            

            next_question_number = int(question) + 1
            # check if next question exists
            if next_question_number in question_dict:
                return JsonResponse({'next_question_number': next_question_number})
            else:
                # No more questions, you can redirect to a finish page or home
                return JsonResponse({'finish': True})
        
        context = {'question': question_object, 'question_number': int(question)}
        return render(request, 'multi_choice_question.html', context)
    
    else: # question type is extended answer
        if request.method == 'POST':
            print(request.POST)
            if request.POST.get('chat') == 'true':
                # chat-bot functionality here
                form = ChatPromptForm(request.POST)
                if form.is_valid():
                    prompt_text = form.cleaned_data['prompt_text']
                    prompt_text = "Be as concise as possible. " + prompt_text
                    response = call_api(prompt_text)
                    # create chat prompt in database
                    haile_user = HaileUser.objects.get(user=request.user)

                    if request.POST.get('review') == 'true':
                        ChatPrompt.objects.create(user_id=haile_user, prompt_text=prompt_text, section_from='extended_answer (review)', ai_response=response)
                    else:
                        ChatPrompt.objects.create(user_id=haile_user, prompt_text=prompt_text, section_from='extended_answer (quiz)', ai_response=response)
                    
                    return JsonResponse({'response': response}, status=200)
                else:
                    return JsonResponse({'errors': form.errors.as_json()}, status=400)

            # handle the checking for correctness here
            correct_answer = question_object.correct_answer
            user_answer = request.POST.get('userResponse')
            similarity = calculate_cosine_similarity(correct_answer, user_answer)
            print(f"SIMILARITY: {similarity}")
            if similarity >= 0.45:
                is_correct = True
            else:
                is_correct = False

            user = request.user
            haile_user = HaileUser.objects.filter(user=user)[0]
            response, created = ExtendedAnswerResponse.objects.get_or_create(
                user=haile_user,
                question=question_object,
                defaults={'is_correct': is_correct, 'user_response': user_answer}
            )

            if not created:
                # Update the existing record
                response.is_correct = is_correct
                response.user_response = user_answer
                response.save()


            next_question_number = int(question) + 1
            # check if next question exists
            if next_question_number in question_dict:
                return JsonResponse({'next_question_number': next_question_number})
            else:
                # No more questions, you can redirect to a finish page or home
                return JsonResponse({'finish': True})
        
        context = {'question': question_object, 'question_number': int(question)}
        return render(request, 'extended_answer.html', context)

def get_question(question_number, question_type):

    if question_type == 'MultipleChoice':
        return MultipleChoiceQuestion.objects.get(question_id=question_number)     
    else: # question_type == 'ExtendedAnswer'
        return ExtendedAnswerQuestion.objects.get(question_id=question_number)


def preprocess_text(text):
    # Tokenize and remove stopwords
    tokens = [word.lower() for word in word_tokenize(text) if word.isalnum() and word.lower() not in stopwords.words('english')]
    
    # Stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]

    return " ".join(stemmed_tokens)

def calculate_cosine_similarity(answer1, answer2):
    # Preprocess the answers
    processed_answer1 = preprocess_text(answer1)
    processed_answer2 = preprocess_text(answer2)

    # Create a CountVectorizer to convert the answers into vectors
    vectorizer = CountVectorizer().fit_transform([processed_answer1, processed_answer2])

    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(vectorizer)
    similarity = similarity_matrix[0, 1]

    return similarity


def review(request):

    # calculate the users final score
    user = HaileUser.objects.filter(user=request.user)[0]
    extended_responses = ExtendedAnswerResponse.objects.filter(user=user, is_correct=True)
    multi_choice_responses = MultipleChoiceResponse.objects.filter(user=user, is_correct=True)
    final_score = len(extended_responses) + len(multi_choice_responses)

    user.final_score = final_score
    user.save()

    context = {'final_score': user.final_score}
    return render(request, 'review.html', context=context)

def review_answer(request, question):
    user = HaileUser.objects.filter(user=request.user)[0]
    question_dict = {1: [1, 'MultipleChoice'], 2: [2, 'MultipleChoice'], 3: [3, 'MultipleChoice'],
                     4: [1, 'ExtendedAnswer'], 5: [2, 'ExtendedAnswer'], 6: [3, 'ExtendedAnswer']}
    

    question_type_number, question_type = question_dict[int(question)]
    question_object = get_question(question_type_number, question_type)
    if question_type == 'MultipleChoice':
        response_object = MultipleChoiceResponse.objects.filter(user=user, question=question_object)[0]
        print(response_object.selected_choice)
    elif question_type == 'ExtendedAnswer':
        response_object = ExtendedAnswerResponse.objects.filter(user=user, question=question_object)[0]

    context = {'question_number': question,'question': question_object, 'response': response_object}

    if question_type == 'ExtendedAnswer':
        return render(request, 'extended_review.html', context)
    else:
        return render(request, 'multi_choice_review.html', context)
