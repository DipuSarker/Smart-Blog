from django.contrib import admin
from .models import Author, Category, Post, Subcribe, Contact, Comment, SubComment

# Register your models here.

admin.site.register(SubComment)

admin.site.register(Subcribe)

admin.site.register(Category)

admin.site.register(Contact)

admin.site.register(Comment)

admin.site.register(Author)

admin.site.register(Post)