from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SendMailToUser(forms.Form):
    firstname = forms.CharField(max_length=60)
    lastname = forms.CharField(max_length=60)
    email = forms.EmailField(help_text='youremail@example.com')
    city = forms.CharField(max_length=25)
    delivery = forms.ChoiceField(choices=(('НП', "Нова Пошта"), ('УП', "Укр Пошта")))

class SignUp(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=250, help_text='youremail@example.com')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')