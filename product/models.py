from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.TextChoices):
    Food ='food'
    Kkids='kids'
    home='home'
    Computer='computer'

class Product(models.Model):
    name = models.CharField(max_length=200, default='', blank=False)
    description = models.TextField(max_length=1000, default='', blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    brand = models.CharField(max_length=200, default='', blank=False)
    category = models.CharField(max_length=200, choices=Category.choices)
    stock = models.IntegerField(default=0)
    createAt = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL)


    def __str__(self):
        return self.name



    
class Review(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField(default=0)
    comment = models.TextField(max_length=1000, default='', blank=False)
    createAt = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment

    



