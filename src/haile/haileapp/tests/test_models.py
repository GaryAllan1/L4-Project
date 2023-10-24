from django.test import TestCase
from haileapp.models import *

class HaileUserTestCase(TestCase):
    def setUp(self):
        HaileUser.objects.create(firstname="John", final_score=100)
        HaileUser.objects.create(firstname="Jane", final_score=90)

    def test_haile_user_names(self):
        john = HaileUser.objects.get(firstname="John")
        jane = HaileUser.objects.get(firstname="Jane")
        self.assertEqual(john.firstname, "John")
        self.assertEqual(jane.firstname, "Jane")


class QuestionTestCase(TestCase):
    def setUp(self):
        Question.objects.create(question_text="What is your name?")
        Question.objects.create(question_text="What is your favorite color?")

    def test_question_text(self):
        name_question = Question.objects.get(question_text="What is your name?")
        color_question = Question.objects.get(question_text="What is your favorite color?")
        self.assertEqual(name_question.question_text, "What is your name?")
        self.assertEqual(color_question.question_text, "What is your favorite color?")

