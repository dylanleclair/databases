from django.urls import path

from . import views

app_name='realbeast'
urlpatterns = [
    # ex: /realbeast/
    path('', views.index, name='index'),

    
    # /realbeast/products/
    path('products/', views.products, name='products'),
    # ex: /realbeast/products/5/
    path('products/<int:product_id>/', views.product_page, name='product_page'),
    path('update_user_info/<int:user_id>/', views.update_user_info, name='update_user_info'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('account/', views.account, name='account'),
    path('cart/',views.cart, name='cart'),
    path('my_login/', views.my_login, name='my_login'),
    path('register/', views.register, name='register'),
    # this code will:
    # match a path with /realbeast/<integer> (ex: localhost:8000/realbeast/1)
    # it will then call the function with the name 'detail' from the module views.detail (see views)
    # this function returns and HTTP request, which we can customize to use
    # a template (see templates/realbeast) to create a custom HTML page using the object 
    # we retreive in the views.detail function. 

    #in summary, we want to query the database using information from the path
    #to serve an HTTP GET request by providing a webpage to the client requesting it

    # this can be plain text, or you can load python data into a dictionary as a context
    # and pass this to the template page, which unpacks and uses the python data 
    # in the http response sent to the user (user is a browser)
]