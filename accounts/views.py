from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# for reset_password_email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django .contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from carts.views import _cart_id
from carts.models import Cart,CartItem
from urllib.parse import urlparse
import requests
def register(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        # print(form.errors)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']
            username=email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.phone_number=phone_number
            user.save()
            messages.success(request,'Registration successful.')
            return redirect('login')
    else:
        form =RegistrationForm()
    context = {
            'form':form,
    }
    return render(request, 'accounts/register.html',context)


def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            try:
                cart =Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists =CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    same_item=[]
                    cart_item =CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        same_item.append(item)
                    user_item =CartItem.objects.filter(user=user)
                    id=[]
                    user_item=[]
                    for item in user_item:
                        user_item.append(item)
                        id.append(item.id)
                    for pr in same_item:
                        if pr in user_item:
                            index=user_item.index(pr)
                            item_id=id[index]
                            item=CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user=user
                            item.save()
                        else:
                            cart_item =CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user=user
                                item.save()

            except:
                pass
            auth.login(request,user)
            messages.success(request,"You are now logged in. ")
            url = request.META.get('HTTP_REFERER')
            try:
                query=requests.utils.urlparse(url).query
                #next/cart/checkout
                params=dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage=params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')


        else:
            messages.error(request,"Invalid login credentials. ")
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out.')

    return redirect('login')
@login_required(login_url='login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')


def forgotPassword(request):
    if request.method=='POST':
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)


            current_site=get_current_site(request)
            mail_subject='Rest Your Password'
            message=render_to_string('accounts/reset_password_email.html',{
            'user':user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request,'Password reset emil has been sent to your email address. ')
            return redirect('login')



        else:
            messages.error(request,'Account does not exist!')
            return redirect('forgotPassword')
    return render(request,'accounts/forgotPassword.html')
def restpassword_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'This link is has been expired!')
        return redirect('login')

def resetPassword(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password == confirm_password:
            uid =request.session.get('uid')
            user =Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset Sucessful')
            return redirect('login')

        else:
            messages.error(request,'Passwords dont match')
            return redirect('resetPassword')
    else:
         return render(request,'accounts/resetPassword.html')
