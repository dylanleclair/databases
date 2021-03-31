# Serializers define the API representation.
from django.contrib.auth.models import User
from realbeast.models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff', 'profile'] 
        # the api representation will have each of the fields above returned!
        # our api supports authentication


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user','total_rewards', 'user_type', 'address', 'phone_number', 'card_no']

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['location', 'owner_id']


class CustomerSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user


class BrandSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Brand
        fields = ['brand']

class SizeSerializer(serializers.ModelSerializer):
    store_id = StoreSerializer()
    class Meta:
        model = Size
        fields = ['store_id','size', 'quantity']

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['product_type']

class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color']

class ProductSerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True,read_only=True)
    sizes = SizeSerializer(many=True,read_only=True)
    product_type = ProductTypeSerializer(many=True,read_only=True)
    colors = ProductColorSerializer(many=True,read_only=True)
    class Meta:
        model = Product
        fields = ['price', 'sex', 'name', 'description', 'brands', 'sizes','product_type','colors'] 


class OrderSerializer(serializers.ModelSerializer):
    user_id = CustomerSerializer()
    store_id = StoreSerializer()
    class Meta:
        model = Order
        fields = ['total_price','order_date','delivery_date','delivery_status','is_restock','rewards_earned', 'user_id', 'store_id']