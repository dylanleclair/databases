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
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta, date
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

    brands = [ x[0] for x in Brand.objects.values_list('brand').distinct() ]

    sexes = ['M', 'F', 'U']

    colors = [ x[0] for x in Color.objects.values_list('color').distinct() ]

    types = [ x[0] for x in ProductType.objects.values_list('product_type').distinct() ]

    context = {
        'message':'Select your filters',
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

    user.first_name = request.POST['firstname']
    user.last_name = request.POST['lastname']
    user.email = request.POST['email']
    user.profile.address = request.POST['address']
    user.profile.phone_number = request.POST['phone']
    user.profile.phone_number = request.POST['card_no']
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
    
    # Create the user's cart
    online = Store.objects.get(location="Online")
    Order.objects.create(user_id=user,store_id=online, delivery_status="Cart")

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
        size = request.POST.getlist('size')
        print(size)
        if not size:
            return HttpResponseRedirect(reverse('realbeast:product_page', args=[product_id]))
        size = size[0]
        # if the user already has item in cart, update quantity
        item_set = Contains.objects.filter(order_id=cart, product_id=product,size=size)
        if item_set.count() > 0:
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
    brands = request.POST.getlist('brands')
    sex = request.POST.getlist('sex')
    types = request.POST.getlist('types')
    colors = request.POST.getlist('colors')

    print(brands)

    products_by_brand = Product.objects.none()
    for brand in brands:
        products_by_brand = products_by_brand.union(Product.objects.filter(brands__brand=brand))

    products_by_sex = Product.objects.none()
    for s in sex:
        products_by_sex = products_by_sex.union(Product.objects.filter(sex=s))

    products_by_type = Product.objects.none()
    for t in types:
        products_by_type = products_by_type.union(Product.objects.filter(product_types__product_type=t))
    
    products_by_color = Product.objects.none()
    for color in colors:
        products_by_color = products_by_color.union(Product.objects.filter(colors__color=color))
    
    products = Product.objects.none().union(products_by_brand,products_by_sex,products_by_type,products_by_color)

    message = "Select your filters"

    if not products:
        message = "Your filters ended up with no results"
        products = Product.objects.all()

    # get a list of products instead!
    template = loader.get_template('realbeast/products.html')

    brands = [ x[0] for x in Brand.objects.values_list('brand').distinct() ]

    sexes = ['M', 'F', 'U']

    colors = [ x[0] for x in Color.objects.values_list('color').distinct() ]

    types = [ x[0] for x in ProductType.objects.values_list('product_type').distinct() ]

    context = {
        'message':message,
        'products':products,
        'brands':brands,
        'sexes':sexes,
        'types':types,
        'colors':colors,
        }

    return HttpResponse(template.render(context, request))

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

# Restock order page 
def restock(request):
    products = Product.objects.all()

    stores = Store.objects.all()

    allProducts = []
    for product in products:

        sizes = Size.objects.filter(product_id=product.id).all()

        prod_size = []

        for size in sizes:

            prod_size.append(size)

        
        prod_obj = {
            'prod': product,
            'product_sizes':prod_size,
        }

        allProducts.append(prod_obj)

    sizes = Size.objects.filter(product_id=product.id)
    context = {
        'products' : allProducts,
        'stores' : stores
    }
    return render(request, 'realbeast/restock.html', context)

def restockItems(request) :
    product = request.POST['prod']
    location = request.POST['Location']
    siz = request.POST.getlist['sizeSelect']
    quantity = request.POST['quantities']

    sizes = Size.objects.filter(product_id = product).filter(size = siz)
    if(not(sizes)):

        temp = Size()
        temp.product_id = product
        temp.size = siz
        temp.store_id = location.id
        temp.save()

    else:
        temp = sizes[0]
        temp.quantity += quantity
        temp.save()   


    return HttpResponseRedirect(reverse('realbeast:products'))





def checkout(request):
    user = request.user # retreive the logged in user
    # find the items in their cart!
    order = Order.objects.filter(user_id=user.id,delivery_status='Cart')[0]
    context = {
        'order_id' :  order.id,
    }
    template = loader.get_template('realbeast/checkout.html')
    return HttpResponse(template.render(context,request))

def finalize_order(request):
    print("YOLO")
    user = request.user
    order = Order.objects.filter(user_id=user.id,delivery_status='Cart')[0]
    # code to finalize the order 
    print(order)
    now = date.today()
    now = now + timedelta(days=5)
    order.delivery_status = 'Shipped'
    order.delivery_date=now
    order.save()
    # verify this is possible
    # update the quantities available
    online = Store.objects.get(location='Online')
    new_cart = Order(user_id=order.user_id,store_id=online,delivery_status='Cart')
    new_cart.save()
    
    return HttpResponseRedirect(reverse('realbeast:products'))
# API VIEWS

#=========================================================
# User API section
#=========================================================

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
        user.save()
        online = Store.objects.get(location="Online")
        # Create the user's cart
        Order.objects.create(user_id=user,store_id=online, delivery_status="Cart")

        data = {
            'user':user,
            'profile': request.data.get('profile'),
            'email':request.data.get('email'),
            'first_name':request.data.get('first_name'),
            'last_name':request.data.get('last_name'),
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
            'email':request.data.get('email'),
            'first_name':request.data.get('first_name'),
            'last_name':request.data.get('last_name'),
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
        if usr.username == 'admin':
            return Response(
            {"res": "Deleting the admin is forbidden!"},
            status=status.HTTP_400_BAD_REQUEST
        )
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
        sizing = Size.objects.get(store_id__location=location, product_id__id=product_id, size=size) 
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

    # add a new location
    def post(self,request, *args, **kwargs):
        '''
        Create a store with given data
        '''


        data = {
            'location' : request.data.get('location'), 
            'owner' : request.data.get('owner'), 
        }
        serializer = StoreSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    def put(self,request, location, *args, **kwargs):
        location = Store.objects.get(location=location)
        if not location:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = {
            'location' : request.data.get('location'), 
            'owner' : request.data.get('owner'), 
        }
        serializer = StoreSerializer(instance=location,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,location, *args, **kwargs):
        location = Store.objects.get(location=location)
        if not location:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if location.location == 'Online':
            return Response(
            {"res": "Deleting the Online store is forbidden!"},
            status=status.HTTP_400_BAD_REQUEST
        )

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

    # Deletes the order, unless it is a cart - in which case, the items are removed from the cart
    def delete(self,request,order_id, *args, **kwargs):
        order = Order.objects.get(id=order_id)
        if not order:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # If the status is a cart, empty out all the items
        # otherwise, delete the order as usual

        if order.delivery_status == 'Cart':
            orders = Contains.objects.filter(order_id=order_id)
            for item in orders:
                item.delete()
            
            return Response(
                {"res": "Cart cleared!"},
                status=status.HTTP_200_OK
            )
        else: 
            order.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class OrderDetailAction(APIView):
    permission_classes = [permissions.IsAuthenticated]
    '''
    Pre-cooked actions that can be performed on each object
    '''

    def get(self,request, order_id,action, *args,**kwargs):
        
        # check the action and perform associated transformation
        # (typically just changes status, maybe dates)
        
        order = Order.objects.get(id=order_id)
        if not order:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if action=='cancel':
            order.delivery_status = 'Cancelled'
            if order.location == "Online" and order.delivery_status == "Cart":
                online = Store.objects.get(location='Online')
                new_cart = Order(user_id=order.user_id,store_id=online,delivery_status='Cart')
                new_cart.save()
        elif action == 'finalize':
            now = date.today()
            now = now + timedelta(days=5)
            order.delivery_status = 'Shipped'
            order.delivery_date=now

            # make sure each product in order is in stock

            valid = True
            contains_set = Contains.objects.filter(order_id=order)
            for item in contains_set:
                quantity_location = Size.get(store_id=order.store_id, size = item.size,quantity=item.quantity)
                if item.quantity > quantity_location:
                    valid = False

            if valid:
                for item in contains_set:
                    quantity_location = Size.get(store_id=order.store_id, size = item.size,quantity=item.quantity)
                    quantity_location.quantity -= item.quantity

            if not valid:
                return Response(
                    {"res": "Not enough quantity to fill order!"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # calculate the price?
            user = User.objects.filter(username=order.username)
            user.total_rewards += order.rewards_earned 
            user.save()
            payment = Payment(payment_type="Credit", amount=order.total_price, order_id = order)
            payment.save()
            # verify this is possible
            # update the quantities available
            if order.delivery_status == "Cart":
                online = Store.objects.get(location='Online')
                new_cart = Order(user_id=order.user_id,store_id=online,delivery_status='Cart')
                new_cart.save()
        
        order.save()
        serializer = OrderSerializer(order, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderItemList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    '''
    Interface for viewing items in an order
    '''
    
    def get(self,request, order_id, *args,**kwargs):
        # views a specific item in a cart
        items = Contains.objects.filter(order_id__id=order_id)
        serializer = ContainsSerializer(items,many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Adds an item to an order
    def post (self,request,order_id,*args, **kwargs):
        data = {
            'product_id' : request.data.get('product_id'),
            'quantity': request.data.get('quantity'),
            'size':request.data.get('size'),
        }
        serializer = ContainsSerializer(data=data,context={'order_id':order_id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderItemDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    '''
    Interface for viewing and editing items in an order
    '''
    def get(self,request, order_id,item_id, *args,**kwargs):
        # views a specific item in a cart
        items = Contains.objects.get(pk=item_id)
        serializer = ContainsSerializer(items, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Updates an item in the cart (usually change in quantity)
    def put (self,request,order_id, item_id, *args, **kwargs):
        '''
        Updates the specified product, if it exists
        '''
        item = Contains.objects.get(pk=item_id)
        if not item:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = {
            # only the sizes are specific to a given store! 
            'product_id' : request.data.get('product_id'), 
            'quantity' : request.data.get('quantity'), 
            'size' : request.data.get('size'), 
        }
        serializer = ContainsSerializer(instance=item, data=data,partial=True )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,order_id,item_id, *args, **kwargs):
        item = Contains.objects.get(pk=item_id, order_id=order_id)
        if not item:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        item.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )