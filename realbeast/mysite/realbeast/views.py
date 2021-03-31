from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from .models import User, Product, Store, Size, Order, Contains
from django.template.backends.django import Template
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth import authenticate, login
from realbeast.serializers import BrandSerializer, CustomerSerializer, OrderSerializer, ProductSerializer, ProfileSerializer, StoreSerializer, UserSerializer
from realbeast.models import Brand, Profile
from rest_framework import viewsets, generics
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

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
    products = Product.objects.all()[:12];
    template = loader.get_template('realbeast/products.html')
    context = {
        'products':products,
    }

    return HttpResponse(template.render(context, request))

# the product page of a specific item
def product_page(request, product_id):
    # retreive the object from the database
    product = Product.objects.filter(id=product_id)[0];
    template = loader.get_template('realbeast/product.html')
    sizes = Size.objects.filter(product_id=product.id)
    stores_list = []
    for size in sizes:
        print(size.store_id.location)
        stores_list.append({
            'location': size.store_id.location,
            'size': size.size,
            'quantity' : size.quantity,       
        })
    instock = len(stores_list) > 0
    context = {
        'product':product,
        'stores':stores_list,
        'instock':instock,
        
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
    username = request.POST['username'];
    email = request.POST['email'];
    password = request.POST['password'];    
    user = User.objects.create_user(username,email,password);
    user.first_name = request.POST['firstname'];
    user.last_name = request.POST['lastname'];
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
        # identify the product
        item = Contains(order_id=cart,product_id=product,quantity=quantity)
        item.save() # save to the database
        
        # TODO: if item already exists in cart, add to the quantity!
        
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
            }
        )

    context = {
        'cart_items': cart_items,
    }
    template = loader.get_template('realbeast/cart.html')
    return HttpResponse(template.render(context, request));


# API VIEWS


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

# the triple quoted comments for each of these are converted to markdown
# which is rendered on the browsable API views
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profiles to be viewed or edited.
    Profiles have a one-to-one relationship with the Users object, which handles authentication. 
    
    Profiles serve to add the information users needs for our project to a user's authentication details. 
    
    This includes: 
    
    - user type
    - addresses
    - rewards points
    - phone numbers
    - and payment information.  
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    #permission_classes = [permissions.IsAuthenticated]

class StoreViewSet(viewsets.ModelViewSet):
    '''
    
    '''
    queryset = Store.objects.all()
    serializer_class = StoreSerializer



class CustomerViewSet(viewsets.ModelViewSet, CountModelMixin):
    '''
    Combines the user and profile objects
    '''
    queryset = User.objects.all()
    serializer_class = CustomerSerializer


class ProductViewSet(viewsets.ModelViewSet, CountModelMixin):
    '''
    Combines the user and profile objects
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class ProductBrandList(generics.ListAPIView):
    serializer_class = Product
    def get_queryset(self):
        return Brand.filter

class OrderViewSet(viewsets.ModelViewSet, CountModelMixin):
    '''
    Combines the user and profile objects
    '''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
