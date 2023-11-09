import os
from haileapp.models import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'haile.settings')

def populate():
    quiz = create_quiz("Test Quiz")

    return

def create_quiz(title):
     return Quiz.objects.create(title=title)


if __name__ == "__main__":
    print("Populating database...")
    populate()
    print("Done")