from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import ChatPrompt, HaileUser
 
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'username', 'password1', 'password2')

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "password")

class ChatPromptForm(forms.ModelForm):
    class Meta:
        model = ChatPrompt
        fields = ('prompt_text',)

class HasStudiedForm(forms.ModelForm):

    class Meta:
        model = HaileUser
        fields = ('has_studied',)