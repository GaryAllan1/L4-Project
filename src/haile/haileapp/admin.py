from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(HaileUser)

admin.site.register(ChatPrompt)

admin.site.register(Question)

admin.site.register(Response)

admin.site.register(Quiz)

