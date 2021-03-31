
import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
#####################################################

# The models representing the data in our database. 
# This is carried over to the actual database for us by Django!
# We just have to define the objects and we're set.
# 
# 
# Todo: 
#   - Add __str__() function for common types (more readable) 

#####################################################


# Note: all IDs are created by default for us by Django! They are referenced by ID or pk. 

class Profile(models.Model): # extends Django user / auth
    user = models.OneToOneField(User, on_delete=models.CASCADE) # links to django user management
    total_rewards = models.IntegerField(default=0)
    user_type = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    card_no = models.CharField(max_length=200) # should this be an integer?
    # use User.is_staff to check if staff
    # use User.is_superuser to check if superuser

@receiver(post_save, sender=User)
def create_user_profile(sender,instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance) # creates a profile for every new user


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

''' - SIMPLIFIED into profile
# defining the multivalued user attributes
class Address(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
'''

'''simplified into profile'''

''' SIMPLIFIED into profile
# defining the multivalued user attributes
class PhoneNumber(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=200) # should this be an integer?
'''
''' SIMPLIFIED into profile -> see user_type
# defining user classes
class Owner(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
# defining user classes
class Employee(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
'''

class Store(models.Model):
    location = models.CharField(max_length=200)
    owner_id = models.ForeignKey(User,on_delete=models.CASCADE) 
    # I removed number of employees, since this can be found by querying works at. 

# works at relation - for employees only
class WorksAt(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Order(models.Model):
    total_price = models.DecimalField(default=0, max_digits=20, decimal_places=2, )
    order_date = models.DateTimeField('date ordered')
    delivery_date = models.DateField('expected delivery date')
    delivery_status = models.CharField(max_length=200) # cart indicates the order is yet to be made
    is_restock = models.BooleanField(default=False)
    rewards_earned = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) # if the user is deleted, delete their orders
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE) # if the store is closed, set the store to null

class Payment(models.Model):
    payment_type = models.CharField(max_length=200)
    amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)# deletes a payment if the order is cancelled

# deprecated - combined into size (ie: quantity of size of each product at each store -- SEE: Size)
'''class InStock(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)'''

class Product(models.Model):
    #size = models.CharField(max_length=200) # delete?
    price = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    sex = models.CharField(max_length=1) # only supports 1 letter (m/f)
    name = models.CharField(max_length=200)
    img_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    caption = models.CharField(max_length=200)
    # add description / details!
    # defining multivalued attributes for products

class Details(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

class Brand(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='brands')
    brand = models.CharField(max_length=200)

class Size(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE,related_name='store') # if store is deleted, delete this too

class ProductType(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_type')
    product_type = models.CharField(max_length=200)

class Color(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    color = models.CharField(max_length=200)


# m:n relationships
class Contains(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='contains')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1)

#m:n relationships
class Modifies(models.Model):
    modification_type = models.CharField(max_length=200)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField('time of edit')


