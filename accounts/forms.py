from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import BankAccount

class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='Optional.')
    last_name = forms.CharField(max_length=30, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    bank_account = forms.CharField()
    pin = forms.CharField()
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2','bank_account','pin']

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Username'}))
    password = forms.CharField(label="Confirm Password", max_length=20,widget=forms.TextInput(attrs={'class': 'form-control','type':'password','placeholder':'Enter Password'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())