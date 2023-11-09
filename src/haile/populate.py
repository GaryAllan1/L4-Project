import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'haile.settings')
import django
django.setup()
from haileapp.models import *

def populate():
    quiz = create_quiz("Test Quiz")

    # Create some multiple choice questions
    multi_text = "What is the capital of France?"
    choices = ['Berlin', 'London', 'Paris', 'Madrid']
    correct_choice = 2
    create_multiple_choice_question(multi_text, quiz, choices, correct_choice)

    multi_text = "Which element has the chemical symbol 'O'?"
    choices = ['Oxygen', 'Osmium', 'Ozone', 'Oslo']
    correct_choice = 0
    create_multiple_choice_question(multi_text, quiz, choices, correct_choice)

    multi_text = "Who was the first President of the United States?"
    choices = ['John Adams', 'Thomas Jefferson', 'George Washington', 'Benjamin Franklin']
    correct_choice = 2
    create_multiple_choice_question(multi_text, quiz, choices, correct_choice)

    # Create some extended answer questions
    question_text = "What is the main theme of George Orwell's '1984'?"
    correct_answer = "Dystopian society and government surveillance"
    create_extended_question(question_text, quiz, correct_answer)

    question_text = "State Newton's First Law of Motion."
    correct_answer = "An object at rest stays at rest and an object in motion stays in motion with the same speed and in the same direction unless acted upon by an unbalanced external force."
    create_extended_question(question_text, quiz, correct_answer)

    question_text = "Describe caching in an operating system"
    correct_answer = "Caching in an operating system involves storing frequently accessed data in a faster, smaller memory space to reduce the time it takes to retrieve that data, enhancing overall system performance."
    create_extended_question(question_text, quiz, correct_answer)


    return

def create_quiz(title):
     return Quiz.objects.create(title=title)

def create_multiple_choice_question(question_text, quiz, choices, correct_choice):
    MultipleChoiceQuestion.objects.create(question_text=question_text, quiz=quiz,
                                          choices=choices, correct_choice=correct_choice)

def create_extended_question(question_text, quiz, correct_answer):
    ExtendedAnswerQuestion.objects.create(question_text=question_text, quiz=quiz,
                                          correct_answer=correct_answer)

if __name__ == "__main__":
    print("Populating database...")
    populate()
    print("Done")