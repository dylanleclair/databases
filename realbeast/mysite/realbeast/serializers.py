# Serializers define the API representation.
from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers

# Used by the REST API 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff', 'profile', 'first_name', 'last_name'] 
        # the api representation will have each of the fields above returned!
        # our api supports authentication


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['total_rewards', 'user_type', 'address', 'phone_number', 'card_no']

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['location', 'owner_id']

'''
Is the main serialization class for users - combines UserSerializer and Profile serializer into one. 
'''
class CustomerSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(partial=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile']

    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    # used to update the a profile / user data
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        
        if not profile_data == None:
            # update the profile data
            profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        
        profile.total_rewards = profile_data.get('total_rewards', profile.total_rewards)
        profile.address = profile_data.get('address', profile.address)
        profile.phone_number = profile_data.get('phone_number', profile.phone_number)
        profile.card_no = profile_data.get('card_no', profile.card_no)
        profile.user_type = profile_data.get('user_type', profile.user_type)

        profile.save()

        return instance

class BrandSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Brand
        fields = ['brand']



class SizeSerializerWithStore(serializers.ModelSerializer):
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
    product_type = ProductTypeSerializer(many=True,read_only=True)
    colors = ProductColorSerializer(many=True,read_only=True)
    class Meta:
        model = Product
        fields = ['id','price', 'sex', 'name', 'description','caption', 'brands','product_type','colors'] 


class SizeSerializer(serializers.ModelSerializer):
    #store_id = StoreSerializer()
    class Meta:
        model = Size
        fields = ['size', 'quantity']

'''
A variation of the product serializer that focuses on the store
'''
class ProductStoreSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(many=True,read_only=True)
    class Meta:
        model = Product
        fields = ['id','price', 'sex', 'name', 'description','sizes'] 


class OrderSerializer(serializers.ModelSerializer):
    user_id = CustomerSerializer()
    store_id = StoreSerializer()
    class Meta:
        model = Order
        fields = ['total_price','order_date','delivery_date','delivery_status','is_restock','rewards_earned', 'user_id', 'store_id']



