from django import forms
from django.db import models

class TransferForm(forms.Form):
    bankaccnum = forms.CharField(label='Bank Account Number', max_length=20,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Bank Account Number'}))

class Transfer2Form(forms.Form):
    amount = forms.DecimalField(label="Amount",decimal_places = 2,widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Enter Amount'}))
    pin = forms.CharField()
    
class DepositAndWithdrawForm(forms.Form):
    amount = forms.DecimalField(label="Amount",decimal_places = 2,widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Enter Amount'}))

class AddBankAccForm(forms.Form):
    bankaccnum = forms.CharField(label='Bank Account Number', max_length=20,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Bank Account Number'}))
    pin = forms.CharField()

class EnterBankAccForm(forms.Form):
    bankaccnum = forms.CharField(label='Bank Account Number', max_length=20,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Bank Account Number'}))

class AddFavoriteForm(forms.Form):
    bankaccnum = forms.CharField(label='Bank Account Number', max_length=20,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Bank Account Number'}))
    name = forms.CharField(label='name', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Name'}))