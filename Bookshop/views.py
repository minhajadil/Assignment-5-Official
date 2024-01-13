from django.shortcuts import render
from Books.models import Book
from Books.models import Category


def home(request, category_slug=None):
    data = Book.objects.all()
 
    if category_slug is not None:
        category = Category.objects.get(slug= category_slug)
        data = Book.objects.filter(category=category)

    category = Category.objects.all()



    return render(request,'home.html',{'data':data,'categories':category})