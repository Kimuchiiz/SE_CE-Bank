from django.db import models
from accounts.models import BankAccount

# Create your models here.
class TransactionLog(models.Model):
    frombankaccount = models.ForeignKey(BankAccount,on_delete=models.SET_NULL,null=True,related_name='frombankaccount')
    tobankaccount = models.ForeignKey(BankAccount,on_delete=models.SET_NULL,null=True,related_name='tobankaccount')
    transactiontype = models.CharField(max_length=30) 
    number = models.CharField(max_length=30, unique = True)
    datetime = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
        ) 

class Favorite(models.Model):
    bankaccount = models.ForeignKey(BankAccount,on_delete=models.CASCADE,null=True,related_name='fav')
    favbankaccount = models.ForeignKey(BankAccount,on_delete=models.CASCADE,null=True,related_name='favbankaccount')
    name = models.CharField(max_length=100, default='')