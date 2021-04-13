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
    path('api/sizes/<str:location>/', ProductStoreList.as_view(), name="productsatstore"),
    path('api/sizes/<str:location>/<int:product_id>', ProductStoreDetail.as_view(), name="products"),
    path('api/stores/<str:location>/', StoreAPIView.as_view(), name="store"),
    path('api/stores/', StoreAPIView.as_view(), name="stores"),
    path('api/products/', ProductList.as_view(), name='products')
]
