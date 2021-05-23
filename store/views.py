from django.shortcuts import render,get_object_or_404,redirect
from store.models import Book,ReviewRating
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import ReviewForm
from orders.models import OrderProduct
from django.contrib import messages
def store(request,category_slug=None):
    categories=None
    books=None
    if category_slug !=None:
         categories=get_object_or_404(Category,slug=category_slug)
         books=Book.objects.filter(category=categories,is_available=True)
         paginator=Paginator(books,3)
         page=request.GET.get('page')
         paged_prodcuts=paginator.get_page(page)
         books_count=books.count()
    else:
        books=Book.objects.all().filter(is_available=True).order_by('id')
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
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user,product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None

    else:
        orderproduct = None
    reviews =ReviewRating.objects.filter(product_id=single_product.id,status=True )


    context={
        'single_product':single_product,
        'in_cart':in_cart,
        'orderproduct':orderproduct,
        'reviews':reviews,

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
def submit_review(request,product_id):
    if request.method=='POST':
        url =request.META.get('HTTP_REFERER')
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            form=ReviewForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,'Thank you! Your review has been updated.')
            return redirect(url)


        except ReviewRating.DoesNotExist:
            form=ReviewForm(request.POST)
            if form.is_valid():
                data=ReviewRating()
                data.subject=form.cleaned_data['subject']
                data.rating=form.cleaned_data['rating']
                data.review=form.cleaned_data['review']
                data.ip=request.META.get('REMOTE_ADDR')
                data.product_id=product_id
                data.user_id=request.user.id
                data.save()
                messages.success(request,'Thank you! Your review has been submitted.')
                return redirect(url)
