from django.contrib import admin
from .models import Book, ReviewRating
class BookAdmin(admin.ModelAdmin):
   list_display=('book_name','auther_name','price' ,'stock','category','publish_date','is_available')
   prepopulated_fields={'slug':('book_name',)}
admin.site.register(Book,BookAdmin)
admin.site.register(ReviewRating)
