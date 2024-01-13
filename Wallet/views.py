from django.shortcuts import render,redirect
from .forms import Deposit
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
# Create your views here.


def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()





@login_required(login_url='login')
def deposit(request):
    form = Deposit()
    if request.method=='POST':
        form = Deposit(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user = request.user
            user.account.balance+=amount
            user.account.save()
            messages.success(request,'Money has been deposited successfully')
            send_transaction_email(user, amount, 'Money Deposit Confirmation', 'deposit_email.html')

            return redirect('homepage')
    return render(request,'deposit.html', {'form':form})


