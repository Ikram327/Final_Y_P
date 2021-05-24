from django.shortcuts import render
from store.models import Book,ReviewRating

def home(requests):
    books=Book.objects.all().filter(is_available=True).order_by('publish_date')
    for product in books:
        reviews =ReviewRating.objects.filter(product_id=product.id,status=True )
    context={
    'books':books,
    'reviews':reviews,
    }
    return render(requests,'home.html',context)
