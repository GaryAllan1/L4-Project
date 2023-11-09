from django.db import models
from django.contrib.auth.models import User


class HaileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    final_score = models.IntegerField(null=True)

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

class ExtendedAnswerResponse(Response):
    question = models.ForeignKey(ExtendedAnswerQuestion, on_delete=models.CASCADE)

