from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("study/", views.study, name="study"),
    path("quiz_intro", views.quiz_intro, name="quiz_intro"),
    path("signup", views.signup, name="signup"),
]