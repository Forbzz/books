from django.contrib import admin
from .models import Book, Author, Genre, Reviews, Profile, Mail


class CollectionMail(admin.ModelAdmin):
    filter_vertical = ('users',)


admin.site.register(Mail, CollectionMail)

admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Reviews)

