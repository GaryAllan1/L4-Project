from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(HaileUser)

admin.site.register(ChatPrompt)

admin.site.register(MultipleChoiceQuestion)
admin.site.register(ExtendedAnswerQuestion)

admin.site.register(MultipleChoiceResponse)
admin.site.register(ExtendedAnswerResponse)

admin.site.register(Quiz)

