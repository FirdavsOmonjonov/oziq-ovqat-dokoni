from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
# Create your models here.


class Category(models.Model):
    """Category model"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Kategoriya")
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True,
                               related_name='subcategories')

    def __str__(self):
        return self.name


FILTER_CHOICES = {
    'po': 'Popularity',
    'org': 'Organic',
    'fan': 'Fantastic'
}


class Product(models.Model):
    """Product model"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoriya")
    filter_choice = models.CharField(max_length=3, choices=FILTER_CHOICES, null=True)
    name = models.CharField(max_length=255, verbose_name="Nomi")
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    discount = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', verbose_name="Rasmi")
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name}: {self.rating}"

