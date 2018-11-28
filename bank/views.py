from django.shortcuts import render
from django.db import models
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from .forms import TransferForm,Transfer2Form, AddBankAccForm,DepositAndWithdrawForm,EnterBankAccForm,AddFavoriteForm
from accounts.models import BankAccount
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TransactionLog,Favorite

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def Index(request):
    if request.user.is_staff:
        template_name = 'bank/staff_index.html'
        return render(request,template_name,{'staff':request.user})
    else:
        template_name = 'bank/index.html'
        all_bankaccounts = request.user.bankaccount_set.all()
        return render(request,template_name,{'all_bankaccounts':all_bankaccounts})

@login_required
def TransactionHistory(request,bankaccount_id):
        if request.user.is_staff:
            template_name = 'bank/staff_transactionhistory.html'
        else:
            template_name = 'bank/transactionhistory.html'
        bankaccount = BankAccount.objects.get(id=bankaccount_id)
        if (request.user.is_staff) or (request.user.bankaccount_set.get(id = bankaccount_id) is not None):
            fromtransactionlogs = bankaccount.frombankaccount.all()
            totransactionlogs = bankaccount.tobankaccount.all()
            all_transactionlogs = fromtransactionlogs | totransactionlogs
            all_transactionlogs = all_transactionlogs.distinct().order_by('-datetime')
            return render(request,template_name,{'all_transactionlogs':all_transactionlogs,'bankaccount_id':bankaccount_id})

@login_required
def Detail(request,bankaccount_id):
    if request.user.is_staff:
        template_name = 'bank/staff_detail.html'
        return render(request,template_name,{'bankaccount':BankAccount.objects.get(id = bankaccount_id),'bankaccount_id':bankaccount_id})
    if request.user.bankaccount_set.get(id = bankaccount_id) is not None:
        template_name = 'bank/detail.html'
        return render(request,template_name,{'bankaccount':BankAccount.objects.get(id = bankaccount_id),'bankaccount_id':bankaccount_id})

@login_required
def AddBankAccount(request):
    form = AddBankAccForm()
    template_name = 'bank/addbankacc.html'

    if request.method == 'POST':
        addbankaccForm = AddBankAccForm(request.POST)

        if addbankaccForm.is_valid():
            try:
                bankaccount = BankAccount.objects.get(number=addbankaccForm.cleaned_data['bankaccnum'])
            except ObjectDoesNotExist:
                return render(request,template_name,{'error_message':'Invalid Bank Account Number','form':form})

            pin = addbankaccForm.cleaned_data['pin']

            if bankaccount.pin == pin:
                    bankaccount.user.add(request.user)
                    bankaccount.save()
                    return redirect('bank:index') 
            else:
                return render(request,template_name,{'error_message':'Invalid PIN','form':form})
        else: 
            return render(request,template_name,{'form':form})

    else:
         return render(request,template_name,{'form':form})

@login_required
def Delete(request,bankaccount_id):
    bankaccount = BankAccount.objects.get(id=bankaccount_id)
    bankaccount.user.remove(request.user)
    bankaccount.save()
    return redirect('bank:index') 

@login_required
def Transfer(request,bankaccount_id):
    form = TransferForm()
    if request.user.is_staff:
        template_name = 'bank/staff_transfer.html'
    else:
        template_name = 'bank/transfer.html'
    frombankaccount = BankAccount.objects.get(id=bankaccount_id)
    if (request.user.is_staff) or (request.user.bankaccount_set.get(id = bankaccount_id) is not None):
        if request.method == 'POST':
            transferForm = TransferForm(request.POST)    
            if transferForm.is_valid():
                try:
                    tobankaccount = BankAccount.objects.get(number=transferForm.cleaned_data['bankaccnum'])
                except ObjectDoesNotExist:
                    return render(request,template_name,{'error_message':'Invalid Bank Account Number','form':form,'bankaccount':frombankaccount,'bankaccount_id':bankaccount_id})
                if tobankaccount == frombankaccount:
                    return render(request,template_name,{'error_message':"Can't Transfer to itself",'form':form,'bankaccount':frombankaccount,'bankaccount_id':bankaccount_id})   
                return redirect('bank:transfer2',bankaccount_id,tobankaccount.pk) 
            else: 
                return render(request,template_name,{'form':form,'bankaccount':frombankaccount,'bankaccount_id':bankaccount_id})
        else:
            return render(request,template_name,{'form':form, 'bankaccount':frombankaccount,'bankaccount_id':bankaccount_id})
    else:
        return redirect('bank:index') 

@login_required
def Transfer2(request,bankaccount_id,tobankaccount_id):
    form = Transfer2Form()
    if request.user.is_staff:
        template_name = 'bank/staff_transfer2.html'
    else:
        template_name = 'bank/transfer2.html'
    frombankaccount = BankAccount.objects.get(id=bankaccount_id)
    tobankaccount = BankAccount.objects.get(id=tobankaccount_id)
    if (request.user.is_staff) or (request.user.bankaccount_set.get(id = bankaccount_id) is not None):
        if request.method == 'POST':
            transfer2Form = Transfer2Form(request.POST)    
            if transfer2Form.is_valid():
                amount = transfer2Form.cleaned_data['amount']
                pin = transfer2Form.cleaned_data['pin']
                if tobankaccount == frombankaccount:
                    return render(request,template_name,{'error_message':"Can't Transfer to itself",'form':form,'bankaccount':frombankaccount,'tobankaccount':tobankaccount,'bankaccount_id':bankaccount_id})
                if amount > 0:
                    if(frombankaccount.pin == pin):
                        if(frombankaccount.balance >= amount):
                            frombankaccount.balance -= amount
                            tobankaccount.balance += amount
                            frombankaccount.save()
                            tobankaccount.save()
                            transactionlog = TransactionLog()
                            transactionlog.frombankaccount = frombankaccount
                            transactionlog.tobankaccount = tobankaccount
                            transactionlog.amount = amount
                            transactionlog.transactiontype = 'Transfer'
                            transactionlog.save()
                            transactionlog.number = str(transactionlog.pk).zfill(10)
                            transactionlog.save()
                            return redirect('bank:receipt',bankaccount_id,transactionlog.pk) 
                        else:
                            return render(request,template_name,{'error_message':'Not Enough Balance','form':form,'bankaccount':frombankaccount,'tobankaccount':tobankaccount,'bankaccount_id':bankaccount_id})
                    else:
                        return render(request,template_name,{'error_message':'Invalid PIN','form':form,'bankaccount':frombankaccount,'tobankaccount':tobankaccount,'bankaccount_id':bankaccount_id})
                else:
                    return render(request,template_name,{'error_message':'Amount Must be > 0','form':form,'bankaccount':frombankaccount,'tobankaccount':tobankaccount,'bankaccount_id':bankaccount_id})
            else: 
                return render(request,template_name,{'form':form,'bankaccount':frombankaccount,'tobankaccount':tobankaccount,'bankaccount_id':bankaccount_id})
        else: 
            return render(request,template_name,{'form':form,'bankaccount':frombankaccount,'tobankaccount':tobankaccount,'bankaccount_id':bankaccount_id})
    else:
        return redirect('bank:index') 

@staff_member_required
def Deposit(request,bankaccount_id):
    form = DepositAndWithdrawForm()
    template_name = 'bank/deposit.html'
    bankaccount = BankAccount.objects.get(id=bankaccount_id)

    if request.method == 'POST':
        depositForm = DepositAndWithdrawForm(request.POST)
        
        if depositForm.is_valid():
            amount = depositForm.cleaned_data['amount']

            if amount > 0:
                bankaccount.balance += amount
                bankaccount.save()
                transactionlog = TransactionLog()
                transactionlog.tobankaccount = bankaccount
                transactionlog.amount = amount
                transactionlog.transactiontype = 'Deposit'
                transactionlog.save()
                transactionlog.number = str(transactionlog.pk).zfill(10)
                transactionlog.save()
                return redirect('bank:receipt',bankaccount_id,transactionlog.pk) 
            else:
                return render(request,template_name,{'error_message':'Amount Must be > 0','form':form,'bankaccount':bankaccount,'bankaccount_id':bankaccount_id})
        else: 
            return render(request,template_name,{'form':form,'bankaccount':bankaccount,'bankaccount_id':bankaccount_id})

    else:
         return render(request,template_name,{'form':form,'bankaccount':bankaccount,'bankaccount_id':bankaccount_id})

@staff_member_required
def Withdraw(request,bankaccount_id):
    form = DepositAndWithdrawForm()
    template_name = 'bank/withdraw.html'
    bankaccount = BankAccount.objects.get(id=bankaccount_id)

    if request.method == 'POST':
        withdrawForm = DepositAndWithdrawForm(request.POST)
        
        if withdrawForm.is_valid():
            amount = withdrawForm.cleaned_data['amount']

            if amount > 0:
                if bankaccount.balance < amount:
                    return render(request,template_name,{'error_message':'Not enough balance','form':form,'bankaccount':bankaccount,'bankaccount_id':bankaccount_id})
                else:
                    bankaccount.balance -= amount
                    bankaccount.save()
                    transactionlog = TransactionLog()
                    transactionlog.frombankaccount = bankaccount
                    transactionlog.amount = amount
                    transactionlog.transactiontype = 'Withdraw'
                    transactionlog.save()
                    transactionlog.number = str(transactionlog.pk).zfill(10)
                    transactionlog.save()
                    return redirect('bank:receipt',bankaccount_id,transactionlog.pk) 
            else:
                return render(request,template_name,{'error_message':'Amount Must be > 0','form':form,'bankaccount':bankaccount,'bankaccount_id':bankaccount_id})
        else: 
            return render(request,template_name,{'form':form,'bankaccount':bankaccount,'bankaccount_id':bankaccount_id})

    else:
         return render(request,template_name,{'form':form,'bankaccount':bankaccount,'bankaccount_id':bankaccount_id})


@login_required
def Receipt(request, bankaccount_id, transactionlog_id):
    if request.user.is_staff:
        template_name = 'bank/staff_receipt.html'
        bankaccount = BankAccount.objects.get(id=bankaccount_id)
    else:
        template_name = 'bank/receipt.html'
        bankaccount = request.user.bankaccount_set.get(id = bankaccount_id)
    transactionlog = TransactionLog.objects.get(id = transactionlog_id)
    if (bankaccount is not None) and (transactionlog.tobankaccount == bankaccount or transactionlog.frombankaccount == bankaccount):
            return render(request,template_name,{'transactionlog':transactionlog,'bankaccount_id':bankaccount_id})
    
@staff_member_required
def EnterBankAcc(request):
    form = EnterBankAccForm()
    template_name = 'bank/enterbankacc.html'
    if request.method == 'POST':
        enterbankaccForm = EnterBankAccForm(request.POST)
        
        if enterbankaccForm.is_valid():
            try:
                bankaccount = BankAccount.objects.get(number=enterbankaccForm.cleaned_data['bankaccnum'])
            except ObjectDoesNotExist:
                return render(request,template_name,{'error_message':'Invalid Bank Account Number','form':form})
            return redirect('bank:bankacc-detail',bankaccount.pk)
        else: 
            return render(request,template_name,{'form':form})

    else:
         return render(request,template_name,{'form':form})

@login_required
def AddFavorite(request,bankaccount_id):
    form = AddFavoriteForm()
    if request.user.is_staff:
        template_name = 'bank/staff_addfavorite.html'
    else:
        template_name = 'bank/addfavorite.html'
    bankaccount = BankAccount.objects.get(id=bankaccount_id)
    if (request.user.is_staff) or (request.user.bankaccount_set.get(id = bankaccount_id) is not None):
        if request.method == 'POST':
            addfavoriteForm = AddFavoriteForm(request.POST)

            if addfavoriteForm.is_valid():
                try:
                    favbankaccount = BankAccount.objects.get(number=addfavoriteForm.cleaned_data['bankaccnum'])
                except ObjectDoesNotExist:
                    return render(request,template_name,{'error_message':'Invalid Bank Account Number','form':form,'bankaccount_id':bankaccount_id})
                if bankaccount == favbankaccount:
                    return render(request,template_name,{'error_message':"Can't add itself to favorite",'form':form,'bankaccount_id':bankaccount_id})
                favorite = Favorite()
                favorite.name = addfavoriteForm.cleaned_data['name']
                favorite.favbankaccount = favbankaccount
                favorite.bankaccount = bankaccount
                favorite.save()
                return redirect('bank:favorite',bankaccount_id) 
            else: 
                return render(request,template_name,{'form':form,'bankaccount_id':bankaccount_id})

        else:
            return render(request,template_name,{'form':form,'bankaccount_id':bankaccount_id})
    else:
        return redirect('bank:index') 

@login_required
def FavoriteView(request,bankaccount_id):
    if request.user.is_staff:
        template_name = 'bank/staff_favorite.html'
    else:
        template_name = 'bank/favorite.html'
    bankaccount = BankAccount.objects.get(id=bankaccount_id)
    if (request.user.is_staff) or (request.user.bankaccount_set.get(id = bankaccount_id) is not None):
        all_favorites = bankaccount.fav.all()
        return render(request,template_name,{'all_favorites':all_favorites,'bankaccount_id':bankaccount_id})

@login_required
def DeleteFavorite(request,bankaccount_id,favorite_id):
    favorite = Favorite.objects.get(id=favorite_id)
    if (request.user.is_staff) or (request.user.bankaccount_set.get(id = bankaccount_id) is not None):
        if(favorite.bankaccount ==  BankAccount.objects.get(id = bankaccount_id)):
            favorite.delete()
            return redirect('bank:favorite',bankaccount_id)