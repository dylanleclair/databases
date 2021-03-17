
import datetime

from django.db import models
from django.utils import timezone


#####################################################

# The models representing the data in our database. 
# This is carried over to the actual database for us by Django!
# We just have to define the objects and we're set.
# 
# 
# Todo: 
#   - Add __str__() function for common types (more readable) 

#####################################################


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Extras(models.Model):
    sample = models.CharField(max_length=200)

# Note: all IDs are created by default for us by Django! They are referenced by ID or pk. 

class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_address = models.CharField(max_length=200)
    total_rewards = models.IntegerField(default=0)
    user_type = models.CharField(max_length=200)

# defining the multivalued user attributes
class Address(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)

# defining the multivalued user attributes
class PaymentInfo(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    card_no = models.CharField(max_length=200) # should this be an integer?

# defining the multivalued user attributes
class PhoneNumber(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=200) # should this be an integer?

# defining user classes
class Owner(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
# defining user classes
class Employee(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    

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
    delivery_status = models.CharField(max_length=200)
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
    # add description / details!
# defining multivalued attributes for products

class Brand(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand = models.CharField(max_length=200)

class Size(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE) # if store is deleted, delete this too

class ProductType(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_type = models.CharField(max_length=200)

class Color(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=200)


# m:n relationships
class Contains(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE) 

#m:n relationships
class Modifies(models.Model):
    modification_type = models.CharField(max_length=200)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField('time of edit')


