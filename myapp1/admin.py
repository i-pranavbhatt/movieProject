from django.contrib import admin
from django.db import models
from .models import movie_type, movie_language, movie_rating_type, Client, movie, m_rating, OrderItem, cart, User, Customer




# Register your models here.
admin.site.register(movie_type)
admin.site.register(movie_language)
admin.site.register(movie_rating_type)
admin.site.register(Client)
admin.site.register(Customer)
admin.site.register(movie)
admin.site.register(m_rating)
admin.site.register(OrderItem)
admin.site.register(cart)


