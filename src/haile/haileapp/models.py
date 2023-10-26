from django.db import models

class HaileUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    final_score = models.IntegerField(null=True)

class ChatPrompt(models.Model):
    prompt_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(HaileUser, on_delete=models.CASCADE)
    prompt_text = models.TextField()
    section_from = models.CharField(max_length=100)

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