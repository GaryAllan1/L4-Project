from django.test import TestCase
from django.contrib.auth.models import User
from haileapp.models import *

class HaileUserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')

    def test_haile_user_creation(self):
        haile_user = HaileUser.objects.create(user=self.user, final_score=42, has_studied=True)
        self.assertEqual(haile_user.user, self.user)
        self.assertEqual(haile_user.final_score, 42)
        self.assertTrue(haile_user.has_studied)

    def test_default_final_score(self):
        default_haile_user = HaileUser.objects.create(user=self.user)
        self.assertEqual(default_haile_user.final_score, 0)

    def test_default_has_studied(self):
        default_haile_user = HaileUser.objects.create(user=self.user)
        self.assertFalse(default_haile_user.has_studied)

    def tearDown(self):
        self.user.delete()

class ChatPromptModelTestCase(TestCase):
    def setUp(self):
        self.user = HaileUser.objects.create(user_id=1, final_score=42, has_studied=True)

    def test_chat_prompt_creation(self):
        chat_prompt = ChatPrompt.objects.create(
            user_id=self.user,
            prompt_text="Test prompt text",
            section_from="Test section",
            ai_response="Test AI response"
        )
        self.assertEqual(chat_prompt.prompt_text, "Test prompt text")
        self.assertEqual(chat_prompt.section_from, "Test section")
        self.assertEqual(chat_prompt.ai_response, "Test AI response")

    def test_default_ai_response(self):
        default_chat_prompt = ChatPrompt.objects.create(
            user_id=self.user,
            prompt_text="Default prompt text",
            section_from="Default section"
        )
        self.assertIsNone(default_chat_prompt.ai_response)

    def tearDown(self):
        self.user.delete()

class QuizModelTestCase(TestCase):
    def test_quiz_creation(self):
        quiz = Quiz.objects.create(title="Sample Quiz")
        self.assertEqual(quiz.title, "Sample Quiz")

    def test_default_quiz_id(self):
        quiz = Quiz.objects.create(title="Another Quiz")
        self.assertIsNotNone(quiz.quiz_id)

    def test_default_title(self):
        quiz = Quiz.objects.create()
        self.assertEqual(quiz.title, "")

class QuestionModelTestCase(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(title="Sample Quiz")

    def test_multiple_choice_question_creation(self):
        choices = ["Option A", "Option B", "Option C"]
        mc_question = MultipleChoiceQuestion.objects.create(
            question_text="What is the capital of France?",
            quiz=self.quiz,
            choices=choices,
            correct_choice=1 
        )
        self.assertEqual(mc_question.question_text, "What is the capital of France?")
        self.assertEqual(mc_question.choices, choices)
        self.assertEqual(mc_question.correct_choice, 1)

    def test_extended_answer_question_creation(self):
        ea_question = ExtendedAnswerQuestion.objects.create(
            question_text="Explain the concept of gravity.",
            quiz=self.quiz,
            correct_answer="Gravity is the force that attracts objects toward each other."
        )
        self.assertEqual(ea_question.question_text, "Explain the concept of gravity.")
        self.assertEqual(ea_question.correct_answer, "Gravity is the force that attracts objects toward each other.")

    def tearDown(self):
        self.quiz.delete()

class ResponseModelTestCase(TestCase):
    def setUp(self):
        self.user = HaileUser.objects.create(user_id=1, final_score=42, has_studied=True)

        self.quiz = Quiz.objects.create(title="Sample Quiz")

        self.mc_question = MultipleChoiceQuestion.objects.create(
            question_text="What is the capital of France?",
            quiz=self.quiz,
            choices=["Paris", "Berlin", "Madrid"],
            correct_choice=0
        )

        self.ea_question = ExtendedAnswerQuestion.objects.create(
            question_text="Explain the concept of gravity.",
            quiz=self.quiz,
            correct_answer="Gravity is the force that attracts objects toward each other."
        )

    def test_multiple_choice_response_creation(self):
        mc_response = MultipleChoiceResponse.objects.create(
            user=self.user,
            question=self.mc_question,
            selected_choice=0  # Assuming Paris is selected
        )
        self.assertEqual(mc_response.question, self.mc_question)
        self.assertEqual(mc_response.selected_choice, 0)

    def test_extended_answer_response_creation(self):
        ea_response = ExtendedAnswerResponse.objects.create(
            user=self.user,
            question=self.ea_question,
            user_response="Gravity is the force that attracts objects toward each other."
        )
        self.assertEqual(ea_response.question, self.ea_question)
        self.assertEqual(ea_response.user_response, "Gravity is the force that attracts objects toward each other.")


    def tearDown(self):
        self.user.delete()
        self.quiz.delete()
        self.mc_question.delete()
        self.ea_question.delete()

