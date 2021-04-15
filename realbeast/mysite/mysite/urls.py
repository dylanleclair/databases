"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mysite import views
from realbeast.views import *
from rest_framework import routers
from mysite import api as myapi

# Routers provide an easy way of automatically determining the URL conf.
router = myapi.DocumentedRouter()
#router.register(r'profiles', ProfileViewSet)
#router.register(r'users', UserViewSet)
#router.register(r'profiles', ProfileViewSet)
#router.register(r'stores', StoreViewSet)
#router.register(r'customers', CustomerViewSet)
#router.register(r'products', ProductViewSet)
#router.register(r'brands', BrandViewSet)
#router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', views.index, name='index'),# directs to root of realbeast
    path('api/',include(router.urls)), # directs to the REST API
    path('realbeast/', include('realbeast.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # adding login functionality!
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/user/', UserAPIView.as_view(), name="user"),
    path('api/sizes/<str:location>/<int:product_id>/', StoreSizeProductDetail.as_view(), name="sizes-location-product"),
    path('api/sizes/<str:location>/<int:product_id>/<str:size>/', StoreSizeEntryDetail.as_view(), name="sizes-location-product-size"),
    path('api/sizes/', SizeList.as_view(), name="sizes"),
    path('api/sizes/<str:location>/', StoreSizeList.as_view(), name="sizes-location"),
    path('api/stores/', StoreList.as_view(), name="stores"),
    path('api/stores/<str:location>/', StoreDetail.as_view(), name="store-detail"),
    path('api/products/', ProductList.as_view(), name='products'),
    path('api/products/<int:product_id>/', ProductDetail.as_view(), name='products-detail'),
    path('api/orders/', UserOrderList.as_view(), name="user-orders"),
    path('api/all-orders/', AllOrderList.as_view(),name="all-orders"),
    path('api/orders/<int:order_id>/',OrderDetail.as_view(),name='order-detail'),
    path('api/orders/<int:order_id>/contains/', OrderItemList.as_view(),name='item-list'),
    path('api/orders/<int:order_id>/contains/<int:item_id>', OrderItemDetail.as_view(),name='item-list-detail'),
    path('api/orders/<int:order_id>/<str:action>/', OrderDetailAction.as_view(), name='order-action'),
   
]
