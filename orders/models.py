from django.db import models
from accounts.models import Account
from store.models import Book
class Order(models.Model):
    STATUS=(
    ('New','New'),
    ('Sent','Sent'),
    ('Completed','Completed'),
    ('Cencelled','Cencelled'),

    )
    user=models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    # payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number=models.CharField(max_length=20)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=15)
    email=models.EmailField(max_length=50)
    address_line_1=models.CharField(max_length=50)
    address_line_2=models.CharField(max_length=50 ,blank=True)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    order_note=models.CharField(max_length=50,blank=True)
    tax=models.FloatField()
    order_total=models.FloatField(default=0.0)
    status=models.CharField(max_length=11,choices=STATUS,default='New')
    ip=models.CharField(blank=True,max_length=20)
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.first_name
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

class OrderProduct(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    user=models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    product=models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    product_price=models.FloatField()
    ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product.book_name
