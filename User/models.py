from django.db import models
from django.contrib.auth.models import User
from Books.models import Book

BORROW_CHOICES = (
    ('Borrowed', 'Borrowed'),
    ('Returned', 'Returned'),
)

class Borrow(models.Model):
    user = models.ForeignKey(User, related_name='borrow', on_delete=models.CASCADE)
    book = models.ForeignKey(Book,related_name='book', on_delete=models.CASCADE)
    type = models.CharField(max_length=8, choices=BORROW_CHOICES)
    time = models.DateTimeField(auto_now_add=True)

    
