from django.shortcuts import render,get_object_or_404
from store.models import Book
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
def store(request,category_slug=None):
    categories=None
    books=None
    if category_slug !=None:
         categories=get_object_or_404(Category,slug=category_slug)
         books=Book.objects.filter(category=categories,is_available=True)
         paginator=Paginator(books,1)
         page=request.GET.get('page')
         paged_prodcuts=paginator.get_page(page)
         books_count=books.count()
    else:
        books=Book.objects.all().filter(is_available=True)
        paginator=Paginator(books,6)
        page=request.GET.get('page')
        paged_prodcuts=paginator.get_page(page)

        books_count=books.count()

    context={
    'books':paged_prodcuts,
    'books_count':books_count,
    }
    return render(request,'store/store.html',context)
def book_detail(request,category_slug,product_slug):
    try:
        single_product=Book.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()

    except Exception as e:
        raise e


    context={
        'single_product':single_product,
        'in_cart':in_cart,

        }
    return render(request,'store/book_detail.html',context)
def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            books=Book.objects.order_by('publish_date').filter(Q(description__icontains=keyword) | Q(book_name__icontains=keyword) | Q(auther_name__icontains=keyword))
            books_count=books.count()
    context={
    'books':books,
    'books_count':books_count,
    }
    return render(request,'store/store.html',context)
