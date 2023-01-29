from django import forms

class SendMailToUser(forms.Form):
    firstname = forms.CharField(max_length=60)
    lastname = forms.CharField(max_length=60)
    email = forms.EmailField(help_text='youremail@example.com')
    city = forms.CharField(max_length=25)
    delivery = forms.ChoiceField(choices=(('НП', "Нова Пошта"), ('УП', "Укр Пошта")))
