from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.
class Book(models.Model):
    book_name=models.CharField(max_length=200,unique=True)
    auther_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(max_length=500,unique=True)
    price=models.IntegerField()
    images=models.ImageField(upload_to='photos/prodcuts')
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    publish_date=models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('book_detail',args=[self.category.slug,self.slug])
    def __str__(self):
        return self.book_name
