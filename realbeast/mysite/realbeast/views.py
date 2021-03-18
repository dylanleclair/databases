from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import User, Product, Store, Size
from django.template.backends.django import Template
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
    user_list = User.objects.all()[:5]

    # get a list of products instead!
    products = Product.objects.all()[:10];
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