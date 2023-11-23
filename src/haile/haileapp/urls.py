from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("study/", views.study, name="study"),
    path("quiz_intro/", views.quiz_intro, name="quiz_intro"),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.user_logout, name="logout"),
    path("login/", views.user_login, name="login"),
    path("quiz/<int:question>/", views.quiz, name="quiz"),
    path("review/", views.review, name="review"),
    path("review_answer/<int:question>/", views.review_answer, name="review_answer"),
]