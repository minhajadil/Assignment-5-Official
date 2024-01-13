from django.shortcuts import render,redirect
from .models import Book,Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from User.models import Borrow
from .forms import CommentForm
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


def send_transaction_email(user, Book, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'book' :Book
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()







def detail(request,id):
    book = Book.objects.get(pk=id)
    print(book.title)
    comments= Comment.objects.filter(book=book) 

    if request.user.is_authenticated :
        has_borrowed = Borrow.objects.filter(user=request.user, book__id=id).exists()
         
        borrowed_count = Borrow.objects.filter(user=request.user,book__id=id, type='Borrowed').count()
        return_count = Borrow.objects.filter(user=request.user,book__id=id, type='Returned').count()

        if borrowed_count > return_count:
            possible_return = True
        else :
            possible_return=False
        return render(request,'book_details.html',{'book':book,'comment':comments,'borrowed':has_borrowed,'possible_return':possible_return})
    else :
        return render(request,'book_details.html',{'book':book,'comment':comments})

        

@login_required(login_url='login')
def buy(request,id):
    book = Book.objects.get(pk=id)
    user = request.user
    
    
    if user.account.balance>=book.price:
        borrowed_count = Borrow.objects.filter(user=request.user,book__id=id, type='Borrowed').count()
        return_count = Borrow.objects.filter(user=request.user,book__id=id, type='Returned').count()

        if borrowed_count == return_count:
            user.account.balance-=book.price
            user.account.save()
            Borrow.objects.create(user=user, type='Borrowed', book=book)
            messages.success(request,'Book Borrowed Successfully')
            send_transaction_email(user, book, 'Book Borrow Confirmation', 'book_borrow.html')
            return redirect('details',id=id)
           
        else:
            messages.error(request,'You must have to return the previous copy before borrowing another copy')
            return redirect('details',id=id)

        


    else :
        messages.error(request, "Not enough Money")
        return redirect('deposit')
    

@login_required(login_url='login')
def returning(request,id):
    book = Book.objects.get(pk=id)
    user = request.user
    borrowed_count = Borrow.objects.filter(user=request.user, type='Borrowed').count()
    return_count = Borrow.objects.filter(user=request.user, type='Returned').count()

    if borrowed_count > return_count:
        user.account.balance+=book.price
        user.account.save()
        messages.success(request,'book returned')
        Borrow.objects.create(user=user, type='Returned', book=book)
        return redirect('details',id=id)
        
    else :
        messages.error(request,'Borrow the book first')
        return redirect('details',id=id)







@login_required(login_url='login')

def comment(request,id):
    form =CommentForm()
    if request.method=='POST':
        form =CommentForm(request.POST)
        if form.is_valid():
            book = Book.objects.get(pk=id)
            com = form.cleaned_data['comment']
            Comment.objects.create(user=request.user,Comment=com , book=book)
            return redirect('details',id=id)
    return render(request,'comment.html',{'form':form})



