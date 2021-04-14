from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from .models import User, Product, Store, Size, Order, Contains, Brand, Profile, Color, ProductType
from django.template.backends.django import Template
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .serializers import *
from rest_framework import generics, permissions, status, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
# Create your views here.

def index(request):
    user_list = User.objects.all()[:5]
    template = loader.get_template('realbeast/realindex.html')
    context = {
        'user_list':user_list,
    }
    return HttpResponse(template.render(context, request))

# the main store page
def products(request):

    # get a list of products instead!
    products = Product.objects.all()[:12]
    template = loader.get_template('realbeast/products.html')

    brands = Brand.objects.all()

    sexes = ['M', 'F', 'U']

    colors = Color.objects.all()

    types = ProductType.objects.all() 

    context = {
        'products':products,
        'brands':brands,
        'sexes':sexes,
        'types':types,
        'colors':colors,
        }

    return HttpResponse(template.render(context, request))

# the product page of a specific item
def product_page(request, product_id):
    # retreive the object from the database
    product = Product.objects.filter(id=product_id)[0];
    template = loader.get_template('realbeast/product.html')
    sizes = Size.objects.filter(product_id=product.id)
    stores_list = [] # location, size and quantity IN STORES
    
    online_list = [] # location, size and quantity ONLINE

    sizes_online = [] # S, M, L, XL, ...
    for size in sizes:
        #print(size.store_id.location)
        size_obj = {
                'location': size.store_id.location,
                'size': size.size,
                'quantity' : size.quantity,       
            }
        if size.store_id.location == 'Online':
            # add online sizes
            sizes_online.append(size.size)
            online_list.append(size_obj)
            
        else: 
            stores_list.append(size_obj)

    available_online =len(online_list) > 0
    instock = len(stores_list) > 0
    context = {
        'product':product,
        'stores':stores_list,
        'instock':instock,
        'online':available_online,
        'online_list': online_list,
        'sizes_online':sizes_online,
    }
    return HttpResponse(template.render(context, request));



# the product page of a specific item
def product_edit(request, product_id):
    # retreive the object from the database
    product = Product.objects.filter(id=product_id)[0];
    template = loader.get_template('realbeast/product-edit.html')
    sizes = Size.objects.filter(product_id=product.id)
    stores_list = [] # location, size and quantity IN STORES
    
    online_list = [] # location, size and quantity ONLINE

    sizes_online = [] # S, M, L, XL, ...
    for size in sizes:
        #print(size.store_id.location)
        size_obj = {
                'location': size.store_id.location,
                'size': size.size,
                'quantity' : size.quantity,       
            }
        if size.store_id.location == 'Online':
            # add online sizes
            sizes_online.append(size.size)
            online_list.append(size_obj)
            
        else: 
            stores_list.append(size_obj)

    available_online =len(online_list) > 0
    instock = len(stores_list) > 0
    context = {
        'product':product,
        'stores':stores_list,
        'instock':instock,
        'online':available_online,
        'online_list': online_list,
        'sizes_online':sizes_online,
    }
    return HttpResponse(template.render(context, request));


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def account(request):
    user = request.user
    template = loader.get_template('realbeast/account.html')
    context = {
        'user':user,
    }
    return HttpResponse(template.render(context, request));

def update_user_info(request, user_id):
    user = get_object_or_404(User,pk=user_id)
    profile = user.profile

    user.username = request.POST['username'];
    user.first_name = request.POST['firstname'];
    user.last_name = request.POST['lastname'];
    user.email = request.POST['email'];
    user.profile.address = request.POST['address']
    user.profile.phone_number = request.POST['phone']
    user.save()
    return HttpResponseRedirect(reverse('realbeast:account'))

def register(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']   
    user = User.objects.create_user(username,email,password)
    user.first_name = request.POST['firstname']
    user.last_name = request.POST['lastname']
    user.profile.address = request.POST['address']
    user.profile.phone_number = request.POST['phone']
    user.profile.card_no = request.POST['card_no']
    user.profile.user_type= "Customer"
    user.save()
    user = authenticate(request,username=username, password=password)
    login(request,user) # log them in!
    return HttpResponseRedirect(reverse('realbeast:products'))

def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        # if the user is authenticated, 
        # find their cart (ie: order with status="Cart")
        # and add (1x) the product to it
        user = request.user
        cart = Order.objects.filter(user_id=user.id,delivery_status='Cart')[0]
        product = Product.objects.get(pk=product_id)
        quantity = request.POST['quantity']
        size = request.POST['size']
        print(size)
        # if the user already has item in cart, update quantity
        item_set = Contains.objects.filter(order_id=cart, product_id=product,size=size)
        if len(item_set) > 0:
            item = item_set[0]
            item.quantity += 1
            item.size = size
            item.save()
            #Size.objects.get(product_id=product, store_id__location='Online')
        else:
        # else, add new entry to the cart
        # identify the product
            item = Contains(order_id=cart,product_id=product,quantity=quantity,size=size)
            item.save() # save to the database
    
        
        return HttpResponseRedirect(reverse('realbeast:product_page', args=[product_id]))

def my_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
        # redirect to the store.
        return HttpResponseRedirect(reverse("realbeast:products"))
    else:
        # Return an 'invalid login' error message.
        raise Http404("Invalid login")

def apply_filters(request):
    raise Http404("Not yet implemented")

def cart(request):
    user = request.user # retreive the logged in user
    # find the items in their cart!
    order = Order.objects.filter(user_id=user.id,delivery_status='Cart')[0]
    # now that we have the order, add all of the products it contains to
    # a context that we can display usintg a table
    cart_items = []
    items = Contains.objects.filter(order_id=order.id)
    for item in items:
        # give the context the product
        product = item.product_id
        # give the context the quantity
        quantity = item.quantity
        cart_items.append(
            {
                'product': product,
                'quantity': quantity,
                'size':item.size,
            }
        )


    # CALCULATE THE TOTALS and include in context

    # calculate subtotal

    # calculate taxes

    # calculate shipping (flat rate cuz ill wanna kms otherwise)

    # grand total

    context = {
        'cart_items': cart_items,
    }
    template = loader.get_template('realbeast/cart.html')
    return HttpResponse(template.render(context, request))


# API VIEWS

#=========================================================
# User API section
#=========================================================
from rest_framework.decorators import action
from rest_framework.response import Response
# https://stackoverflow.com/questions/25151586/django-rest-framework-retrieving-object-count-from-a-model
class CountModelMixin(object):
    """
    Count a queryset.
    """
    @action(detail=False)
    def count(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        content = {'count': queryset.count()}
        return Response(content)

'''
Probably the only thing worth noting from this!

You can make your own views using this!!! 

Will likely use for the rest of the other API endpoints.
'''
class UserAPIView(APIView):
    '''
    Gets the data associated with the logged in user. Supports CRUD. 
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get_user(self,user_id):
        try:
            return User.objects.get(id= user_id)
        except User.DoesNotExist:
            return None
    
    # Used to create a user
    def post(self,request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.create_user(username,email,password)
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.is_staff = request.data.get('is_staff') # determines whether user is staff or not
        data = {
            'user': user,
            'profile': request.data.get('profile'),
            'email':request.data.get('email')
        }
        serializer = CustomerSerializer(instance=user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        #user = authenticate(request,username=username, password=password)
        #login(request,user) # log them in!
        return 
    # Retreives a user's data
    def get(self,request, *args, **kwargs):
        '''
        List profile information for given users
        '''
        
        usr = User.objects.get(id= request.user.id)
        if not usr:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = CustomerSerializer(usr, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Updates a users data
    def put(self,request,*args,**kwargs):
        '''
        Updates the logged in user, if they exist
        '''
        usr = self.get_user(request.user.id)
        if not usr:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = {
            'user': usr,
            'profile': request.data.get('profile'),
            'email':request.data.get('email')
        }
        serializer = CustomerSerializer(instance=usr, data=data,partial=True )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        '''
        Deletes the user
        '''
        usr = self.get_user(request.user.id)
        if not usr:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        usr.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


#=========================================================
# Inventory API section
#=========================================================

class SizeList(APIView):
    '''
    Contains all entries of sizes
    '''
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request, *args, **kwargs):
        sizings = Size.objects.all()
        if not sizings:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = SimpleSizeSerializer(sizings,many=True,context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class StoreSizeList(APIView):
    '''
    Contains size entries by store
    '''
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,location, *args, **kwargs):
        sizings = Size.objects.filter(store_id__location=location)
        if not sizings:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = SimpleSizeSerializer(sizings,many=True,context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# Detail view for a specific product at a given store
# Example url: http://127.0.0.1:8000/api/sizes/Online/2
class StoreSizeProductDetail(APIView):
    '''
    Provides CRUD access to product sizing and quantity data, by store. 
    '''
    permission_classes = [permissions.IsAuthenticated]
    # create a get that takes store and product id as a parameter
    def get(self,request,location, product_id, *args, **kwargs):
        '''
        List product information for a given store
        '''
        sizings = Size.objects.filter(store_id__location=location, product_id__id=product_id) 
        if not sizings:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer =SimpleSizeSerializer(sizings,many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Add a product to the stock of a store
        '''
        data = {
            'location' : request.data.get('location'), 
            'product_id' : request.data.get('product_id'), 
            'size':request.data.get('size'), 
            'quantity':request.data.get('quantity'), 
        }

        serializer = SimpleSizeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Example url: http://127.0.0.1:8000/api/sizes/Market%20Mall/1/S/
# This provides access to the S size of product_id 2 at the Online store
# implements get, put, delete
class StoreSizeEntryDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    '''
    Individual size entries are accessed through this endpoint.
    '''
    # update size information
    def get (self,request,location,product_id,size, *args, **kwargs):
        '''
        Updates the specified product, if it exists
        '''
        sizings = Size.objects.get(store_id__location=location, product_id__id=product_id, size=size) 
        if not sizings:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = SimpleSizeSerializer(sizings,context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request,location,product_id,size,*args,**kwargs):
        '''
        Example JSON:
        {
        "location": "Market Mall",
        "product_id": "1",
        "size": "S",
        "quantity": 10
        }

        The product and size should already exist.

        '''
        sizing = Size.objects.get(store_id__location=location, product_id__id=product_id, size=size) 
        if not sizing:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data = {
            'store_id__location' : request.data.get('location'), 
            'product_id__id' : request.data.get('product_id'), 
            'size':request.data.get('size'), 
            'quantity':request.data.get('quantity'), 
        }

        serializer = SimpleSizeSerializer(instance=sizing,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,location,product_id,size,*args,**kwargs):
        '''
        Removes the product from the store
        '''
        sizings = Size.objects.filter(store_id__location=location, product_id__id=product_id, size=size) 
        if not sizing:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        sizing.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

#=========================================================
# Product API section
#=========================================================
class ProductList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    '''
    A list of all products across all stores, this API endpoint is used to alter data about a product
    
    This includes:
        - brands
        - product type
        - colors
        - description
        - sex
        - price
    '''
    def get(self,request, *args, **kwargs):
        '''
        List product information
        '''
        
        #store = Size.objects.get(store_id__id=store_id)
        #find the sizings and quantities of a product  
        products = Product.objects.all()
        if not products:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = ProductSerializer(products,many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        '''
        Create a product with given product data
        '''
        data = {
            'price' : request.data.get('price'), 
            'sex' : request.data.get('sex'), 
            'name' : request.data.get('name'), 
            'description' : request.data.get('description'), 
            'caption' : request.data.get('caption'), 
            'img_name' : request.data.get('img_name'),
            'brands':request.data.get('brands'), # a JSON array of brands
            'product_types':request.data.get('product_types'), # a JSON array of product types
            'colors':request.data.get('colors'), # a JSON array of colors
        }
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# path:  
# general product management class -- this allows for product data (shared amongst all stores) to be updated
class ProductDetail (APIView):
    '''
    Allows product data to be updated and maintained. Supports CRUD, in addition to some queries. 
    '''
    permission_classes = [permissions.IsAuthenticated]

    # Retreives a product
    def get(self,request,product_id, *args, **kwargs):
        '''
        List product information for a given product
        '''
        product = Product.objects.get(pk=product_id)
        if not product:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = ProductSerializer(product, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Updates a product
    def put (self,request,product_id, *args, **kwargs):
        '''
        Updates the specified product, if it exists
        '''
        product = Product.objects.get(pk=product_id)
        if not product:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = {
            # only the sizes are specific to a given store!
            'price' : request.data.get('price'), 
            'sex' : request.data.get('sex'), 
            'name' : request.data.get('name'), 
            'description' : request.data.get('description'), 
            'caption' : request.data.get('caption'), 
            'brands':request.data.get('brands'), # a JSON array of brands
            'product_types':request.data.get('product_types'), # a JSON array of product types
            'colors':request.data.get('colors'), # a JSON array of colors
        }
        serializer = ProductSerializer(instance=product, data=data,partial=True )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Deletes a product
    def delete(self, request, product_id, *args, **kwargs):
        product = Product.objects.get(pk=product_id)
        if not product:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        product.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
        

#=========================================================
# Store API section
#=========================================================
# path: 'api/stores/'
class StoreList(APIView):    
    '''
    Allows a specific store to be altered. Supports CRUD, in addition to some queries. 
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request, *args, **kwargs):
        '''
        List information for all stores
        '''
        
        #store = Size.objects.get(store_id__id=store_id)
        #find the sizings and quantities of a product 
        store = Store.objects.all() 
        if not store:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = StoreSerializer(store,many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # add post
    #def post(self,request, *args, **kwargs):

# path: 'api/stores/<str:location>/'
# example: http://127.0.0.1:8000/api/stores/Chinook/
class StoreDetail(APIView):    
    '''
    Allows a specific store to be altered. Supports CRUD, in addition to some queries. 
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,location, *args, **kwargs):
        '''
        List information for a given location
        '''
        
        #store = Size.objects.get(store_id__id=store_id)
        #find the sizings and quantities of a product 
        store = Store.objects.get(location=location) 
        if not store:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = StoreSerializer(store, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # add put, delete, etc.
    #def post(self,request, location, *args, **kwargs):


    def delete(self,request,location, *args, **kwargs):
        location = Store.objects.get(location=location)
        if not location:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        location.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


#=========================================================
# Order API section
#=========================================================

class AllOrderList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    '''
    A list of orders for all users - to be accessed by staff
    '''
    def get(self,request, *args, **kwargs):
        '''
        List information for a given location
        '''
        
        #store = Size.objects.get(store_id__id=store_id)
        #find the sizings and quantities of a product 
        orders = Order.objects.all().order_by('order_date')[:10]
        serializer = OrderSerializer(orders,many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserOrderList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    '''
    The authenticated user's own orders
    '''

    # Retreives a user's data
    def get(self,request, *args, **kwargs):
        usr = User.objects.get(id= request.user.id)
        if not usr:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        orders= Order.objects.filter(user_id=usr).order_by('order_date')[:10]
        serializer = OrderSerializer(orders,many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    '''
    Allows an order to be modified
    '''

    def get(self,request, order_id, *args,**kwargs):
        order = Order.objects.get(id=order_id)
        if not order:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = OrderSerializer(order, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)