from django.db import models
from django.contrib.auth.models import User


class HaileUser(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('non_binary', 'Non-Binary'),
        ('other', 'Other/Prefer Not to Say'),
    ]

    LEVEL_CHOICES = [
        (1, 'Level 1'),
        (2, 'Level 2'),
        (3, 'Level 3'),
        (4, 'Level 4'),
        ('FR1', 'Faster Route Level 1'),
        ('FR2', 'Faster Route Level 2'),
        ('FR3', 'Faster Route Level 3'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    final_score = models.IntegerField(default=0)
    has_studied = models.BooleanField(default=False)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    current_level_of_study = models.CharField(max_length=10, choices=LEVEL_CHOICES, null=True, blank=True)

class ChatPrompt(models.Model):
    prompt_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(HaileUser, on_delete=models.CASCADE)
    prompt_text = models.TextField()
    section_from = models.CharField(max_length=100)
    ai_response = models.TextField(null=True, blank=True)

class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)

class Question(models.Model):

    question_id = models.AutoField(primary_key=True)
    question_text = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)

    class Meta:
        abstract = True

class MultipleChoiceQuestion(Question):
    choices = models.JSONField() 
    correct_choice = models.IntegerField()

class ExtendedAnswerQuestion(Question):
    correct_answer = models.TextField()

class Response(models.Model):
    class Meta:
        abstract = True
    
    response_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(HaileUser, on_delete=models.CASCADE)
    is_correct = models.BooleanField(null=True)

class MultipleChoiceResponse(Response):
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)
    selected_choice = models.IntegerField()

    class Meta:
        unique_together = ('user', 'question')

class ExtendedAnswerResponse(Response):
    question = models.ForeignKey(ExtendedAnswerQuestion, on_delete=models.CASCADE)
    user_response = models.TextField(blank=True, null=True)
