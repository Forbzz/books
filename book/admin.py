from django.contrib import admin
from .models import Book,Author,Genre,Reviews,Customer
#DataFlair

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Reviews)
admin.site.register(Customer)

