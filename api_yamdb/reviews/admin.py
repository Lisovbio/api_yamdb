from django.contrib import admin

from .models import Category, Genre, Titles, User, Review, Comment

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Titles)
admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comment)
