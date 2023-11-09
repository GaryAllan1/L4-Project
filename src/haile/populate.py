import os
from haileapp.models import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'haile.settings')

def populate():

    return

def create_quiz(title):
    Quiz.objects.create(title=title)

#def create_question()


if __name__ == "__main__":
    print("Populating database...")
    populate()
    print("Done")