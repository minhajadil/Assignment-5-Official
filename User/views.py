from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import UserForm
from Wallet.models import UserBankAccount
from .models import Borrow


# Create your views here.

class signup_user(CreateView):
    model = User
    template_name = 'signup.html'
    form_class= UserForm
    success_url= reverse_lazy('homepage')
    def form_valid(self, form):
        our_user = super().form_valid(form)
        UserBankAccount.objects.create(user=self.object)
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(self.request, user)

        return our_user
       




class login_user(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return reverse_lazy('homepage')
    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    

@login_required(login_url='login')
def profile(request):
    borrowed_instances = Borrow.objects.filter(user=request.user)
    borrowed_instances_count = Borrow.objects.filter(user=request.user, type='Borrowed').count

    return render(request,'profile.html',{'borrowed_instances' :borrowed_instances,'count':borrowed_instances_count})


@login_required(login_url='login')
def userlogout(request):
    logout(request)
    messages.warning(request,'Logged out Successfully')
    return redirect('homepage')