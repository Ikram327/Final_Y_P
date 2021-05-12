from django.shortcuts import render
from store.models import Book

def home(requests):
    books=Book.objects.all().filter(is_available=True)
    context={
    'books':books,
    }
    return render(requests,'home.html',context)
