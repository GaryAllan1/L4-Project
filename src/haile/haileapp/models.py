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

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_type = models.CharField(max_length=50)
    question_text = models.TextField()
    correct_answer = models.TextField()

class Response(models.Model):
    response_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(HaileUser, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(null=True)

class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)