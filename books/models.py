from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.CharField(max_length=500, default=None)
    price = models.FloatField(null=True, blank=True)
    image_url = models.CharField(max_length=2083, default=False)
    follow_author = models.CharField(max_length=2083, blank=True)
    book_available = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    title = models.CharField(max_length=255, default='Order Title')
    created = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.title