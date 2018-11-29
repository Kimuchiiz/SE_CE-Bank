from django.shortcuts import render
from django.db import models
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import View
from .forms import UserForm,LoginForm
from .models import BankAccount
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# Create your models here.

class UserFormView(View):
    form_class = UserForm
    template_name = 'accounts/registration_form.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            try:
                bankaccount = BankAccount.objects.get(number=form.cleaned_data['bank_account'])
            except ObjectDoesNotExist:
                return render(request,self.template_name,{'error_message':'Invalid Bank Account Number','form':form})
            if bankaccount.pin == form.cleaned_data['pin']:
                user = form.save(commit=False)

                # cleaned (normalized) data
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user.set_password(password)
                user.save()
                bankaccount.user.add(user)
                bankaccount.save()

                #return User objects if credentials are correct
                user = authenticate(username=username, password=password)

                if user is not None:

                    if user.is_active:
                        login(request,user)
                        return redirect('bank:index')

        return render(request,self.template_name,{'form':form})

def Login(request):
    form = LoginForm()
    template_name = 'accounts/login_form.html'

    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            remember_me = loginForm.cleaned_data['remember_me']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    if not remember_me:
                        request.session.set_expiry(0)
                    return redirect('bank:index')
            else: 
                return render(request,template_name,{'error_message':'username and password not match','form':form})
        else: 
            return render(request,template_name,{'form':form})

    else:
        if request.user.is_authenticated:
            return redirect('bank:index')
        return render(request,template_name,{'form':form})

class BankAccountCreate(CreateView):
    model = BankAccount
    fields = ['firstname', 'surname', 'personal_id', 'pin']

    def form_valid(self, form):
        bankaccount = form.save()
        bankaccount.number = str(bankaccount.pk).zfill(10)
        bankaccount.save()

        return redirect('bank:bankacc-detail',bankaccount.id)


@login_required
def AccDetail(request):
        template_name = 'accounts/accdetail.html'
        return render(request,template_name,{'account':request.user})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:acc-detail')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })
