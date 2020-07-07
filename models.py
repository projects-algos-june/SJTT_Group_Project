from django.db import models
from django.contrib.auth.models import User
import re

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fn_input']) < 2:
            errors ['first_name'] = "Please add First Name that contains more the two letters"
        if len(postData['ln_input']) < 2:
            errors ['last_name'] = "Please add a Last Name that contains more the two letters"
        if not EMAIL_REGEX.match(postData['email_input']):
            errors['email'] = 'Please enter a valid Email address!'
        if len(postData['password_input']) < 5:
             errors['password'] = 'Please enter an email that contains 5 or more character'
        if postData['confirmpw_input'] != postData['password_input']:
            errors['confirm_pw'] = "Your password and what you typed in comfirm pw dont match try agian"
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email_input']):
            errors['email'] = 'Please enter a valid Email address!'
        elif not postData['email_input'] != Customer.objects.filter('email'):
            errors['email'] = 'Email not found !'


        if len(postData['password_input']) < 5:
             errors['password'] = 'Please enter an email that contains 5 or more character'
        if postData['confirmpw_input'] != postData['password_input']:
            errors['confirm_pw'] = "Your password and what you typed in comfirm pw dont match try agian"
        return errors

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False)
    images = models.ImageField(null=True)
    # you will get an error in the terminal when trying to use ImageFeild.
    # just 'pip install Pillow' in your env.

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try: 
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
            return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=False)
    zipcode = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address
