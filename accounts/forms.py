from django import forms

class RegisterUserForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    username = forms.CharField(max_length=200)
    email = forms.EmailField()
    password = forms.CharField()

class LoginUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()