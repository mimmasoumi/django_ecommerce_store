from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subcategory')
    title = models.CharField(max_length=200)
    slug = models.SlugField()

    def __str__(self):
        return f'{self.title} of {self.category}'


class Slider(models.Model):

    title = models.CharField(max_length=300, null=True, blank=True)
    description = models.CharField(
        max_length=500, null=True, blank=True)
    link = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField()

    class Meta:
        verbose_name = "Slide"
        verbose_name_plural = "Slides"

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Item(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField()
    description = models.TextField()
    small_description = models.TextField()
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(verbose_name="main image")
    files = models.ManyToManyField('FeedFile')
    detail = models.ManyToManyField('ItemDetails', null=True, blank=True)
    quantity = models.IntegerField()
    visit = models.IntegerField(default=0)
    brand = models.ForeignKey(
        Brand, null=True, blank=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse("shop:detail", kwargs={"pk": self.pk})

    def add_to_cart_url(self):
        return reverse("shop:add_to_cart", kwargs={'slug': self.slug})

    def remove_from_cart_url(self):
        return reverse("shop:remove_from_cart", kwargs={'slug': self.slug})

    def remove_single_from_cart_url(self):
        return reverse("shop:remove_single_from_cart", kwargs={'slug': self.slug})

    def get_discount_percent(self):
        percent = ((self.discount_price * 100) / self.price) - 100
        return f'{int(percent)}%'

    def __str__(self):
        return self.title


class Comments(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    stars = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.username.username


class FeedFile(models.Model):
    file = models.FileField()


class ItemDetails(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)


class OrderedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.item.title}'

    def get_total_price(self):
        if self.item.discount_price:
            total_price = int(self.quantity) * int(self.item.discount_price)
        else:
            total_price = int(self.quantity) * int(self.item.price)
        return total_price


class Shipping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    address = models.CharField(max_length=1000)
    phone = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    zipcode = models.CharField(max_length=250)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderedItem)
    ordered = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total_price = 0
        for item in self.items.all():
            total_price += item.get_total_price()
        return total_price

    def get_total_item_quantity(self):
        total = 0
        for i in self.items.all():
            total += int(i.quantity)

        return total
