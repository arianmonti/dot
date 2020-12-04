from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def return_user(self):
        cleaned_data = super().clean()
        user = authenticate(
            username=cleaned_data.get('username'),
            password=cleaned_data.get('password')
        )
        return user

    def clean(self):
        user = self.return_user()
        if user is None:
            raise ValidationError('Incorrect username or password.')


class RegistrationForm(forms.Form):
    username = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput)


    def create_user(self):
        cleaned_data = super().clean()
        User.objects.create_user(
            username=cleaned_data['username'],
            email=cleaned_data['email'],
            password=cleaned_data['password']
        )

    def clean(self):
        cleaned_data = super().clean()
        user = User.objects.filter(username=cleaned_data.get('username')).first()
        email = User.objects.filter(email=cleaned_data.get('email')).first()
        if user is not None or email is not None:
            raise ValidationError('user exists.')
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise ValidationError('passwords are not same.')
