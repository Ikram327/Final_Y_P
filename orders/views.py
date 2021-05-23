from django.shortcuts import render,redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order
from .models import OrderProduct
from store.models import Book
import datetime
# Create your views here.
def payments(request,total=0,quantity=0):
    current_user=request.user
    tax=0
    grand_total=0
    order=Order.objects.get(user=current_user,is_ordered=False)
    order.is_ordered=True
    order.status='Sent'
    order.save()
    #move the cart item to order product table
    cart_items=CartItem.objects.filter(user=current_user)
    for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.order_id=order.id
        orderproduct.user_id=current_user.id
        orderproduct.product_id=item.product_id
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.price
        orderproduct.ordered=True
        orderproduct.save()

    #reduce the quantity of ordered elements
        product=Book.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    CartItem.objects.filter(user=current_user).delete()
    for cart_item in cart_items:
        total+=(cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax=(2*total)/100
    grand_total=total+tax
    context={
    'order':order,
    'cart_items':cart_items,
    'total':total,
    'tax':tax,
    'grand_total':grand_total,
    }
    return render(request,'orders/order_complete.html',context)




    return redirect('home')
def place_order(request,total=0,quantity=0):
    current_user=request.user
    #if the cart count is less then or equal to zero then redirect to store
    cart_items=CartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    if request.method=='POST':
        form=OrderForm(request.POST)
        # print(form.errors)
        grand_total=0
        tax=0
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
        if form.is_valid():
            #store all the billing information include order table
            data = Order()
            data.user=current_user
            data.first_name= form.cleaned_data['first_name']
            data.last_name= form.cleaned_data['last_name']
            data.phone= form.cleaned_data['phone']
            data.email= form.cleaned_data['email']
            data.address_line_1= form.cleaned_data['address_line_1']
            data.address_line_2= form.cleaned_data['address_line_2']
            data.state= form.cleaned_data['state']
            data.city= form.cleaned_data['city']
            data.order_note= form.cleaned_data['order_note']
            data.order_total =grand_total
            data.tax =tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            # to generate order number
            yr=int(datetime.date.today().strftime('%Y'))
            dt=int(datetime.date.today().strftime('%d'))
            mt=int(datetime.date.today().strftime('%m'))
            d=datetime.date(yr,mt,dt)
            current_date=d.strftime('%Y%m%d')
            order_number=current_date + str(data.id)
            data.order_number=order_number
            data.save()

            order=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context ={
            'order':order,
            'cart_items':cart_items,
            'total':total,
            'tax':tax,
            'grand_total':grand_total,
            }

            return render(request,'orders/payments.html',context)
        else:
            return redirect('checkout')
def order_complete(request):
    return render(request,'orders/order_complete.html')
