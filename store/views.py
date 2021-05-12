from django.shortcuts import render,get_object_or_404
from store.models import Book
from category.models import Category
def store(request,category_slug=None):
    categories=None
    books=None
    if category_slug !=None:
         categories=get_object_or_404(Category,slug=category_slug)
         books=Book.objects.filter(category=categories,is_available=True)
         books_count=books.count()
    else:
        books=Book.objects.all().filter(is_available=True)
        books_count=books.count()

    context={
    'books':books,
    'books_count':books_count,
    }
    return render(request,'store/store.html',context)
def book_detail(request,category_slug,product_slug):
    try:
        single_product=Book.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e


    context={
        'single_product':single_product,
        }
    return render(request,'store/book_detail.html',context)
