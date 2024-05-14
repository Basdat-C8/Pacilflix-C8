from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    country = forms.CharField(label='Negara Asal', max_length=100, required=True)