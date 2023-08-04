from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class OnlineShopModel(models.Model):
    title=models.CharField(max_length=50)
    body=models.TextField(null=True)
    author=models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    picture=models.ImageField(null=True, blank=True)
    price=models.IntegerField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_post', args=[str(self.pk)])


    @property
    def imageURL(self):
        try:
            url=self.picture.url
        except:
            url=''
        return url

class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE , null=True, blank=True)
    name=models.CharField(max_length=200, null=True, )
    phone=models.CharField(max_length=200)
    email=models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    product = models.ForeignKey(OnlineShopModel, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
     total=self.product.price * self.quantity
     return total



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode= models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address




# Create your models here.
