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

        # create a cart for the new user!

        return instance

class BrandSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Brand
        fields = ['brand']

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['product_type']

class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color']





class ProductSerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    product_types = ProductTypeSerializer(many=True)
    colors = ProductColorSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id','price', 'sex', 'name', 'description','caption','img_name', 'brands','product_types','colors'] 

    def create(self, validated_data):
        # update product information
        price = validated_data.get('price', None)
        sex = validated_data.get('sex', None)
        name = validated_data.get('name', None)
        img_name = validated_data.get('img_name', None)
        description = validated_data.get('description', None)
        caption = validated_data.get('caption', None)
        instance = Product.objects.create(price=price, sex=sex,name=name,img_name=img_name,description=description,caption=caption)
        instance.save()
        # support for nested fields (brand, colors, product type)
        brand_data = validated_data.pop('brands')
        color_data = validated_data.pop('colors') 
        type_data = validated_data.pop('product_types')
    
        for item in Brand.objects.filter(product_id=instance):
            item.delete()
        for item in Color.objects.filter(product_id=instance):
            item.delete()
        for item in ProductType.objects.filter(product_id=instance):
            item.delete()
        # Update brands
        for brand in brand_data:
            name = brand.get('brand', None)
            if name:
                # check if exists in database
                if not Brand.objects.filter(product_id=instance, brand=name):
                    Brand.objects.create(product_id=instance, brand=name)
        
        # Update color
        for color in color_data:
            name = color.get('color', None)
            if name:
                if not Color.objects.filter(product_id=instance,color=name):
                    Color.objects.create(product_id=instance, color=name)
        
        # Update type
        for t in type_data:
            name = t.get('product_type', None)
            if name:
                if not ProductType.objects.filter(product_id=instance,product_type=name):
                    ProductType.objects.create(product_id=instance, product_type=name)
        
        return instance

    # code for updating a product
    def update(self, instance, validated_data):

        # support for nested fields (brand, colors, product type)
        brand_data = validated_data.pop('brands')
        color_data = validated_data.pop('colors') 
        type_data = validated_data.pop('product_types')
    
        for item in Brand.objects.filter(product_id=instance):
            item.delete()
        for item in Color.objects.filter(product_id=instance):
            item.delete()
        for item in ProductType.objects.filter(product_id=instance):
            item.delete()
        # Update brands
        for brand in brand_data:
            name = brand.get('brand', None)
            if name:
                # check if exists in database
                if not Brand.objects.filter(product_id=instance, brand=name):
                    Brand.objects.create(product_id=instance, brand=name)
        
        # Update color
        for color in color_data:
            name = color.get('color', None)
            if name:
                if not Color.objects.filter(product_id=instance,color=name):
                    Color.objects.create(product_id=instance, color=name)
        
        # Update type
        for t in type_data:
            name = t.get('product_type', None)
            if name:
                if not ProductType.objects.filter(product_id=instance,product_type=name):
                    ProductType.objects.create(product_id=instance, product_type=name)
        

        # update product information
        instance.price = validated_data.get('price', instance.price)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.name = validated_data.get('name', instance.name)
        instance.img_name = validated_data.get('img_name', instance.img_name)
        instance.description = validated_data.get('description', instance.description)
        instance.caption = validated_data.get('caption', instance.caption)
        instance.save()

        return instance


class SizeSerializer(serializers.ModelSerializer):
    #store_id = store_id.location
    class Meta:
        model = Size
        fields = ['store_id','size', 'quantity']

'''
A variation of the product serializer that focuses on the store
'''
class ProductStoreSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(many=True,read_only=True)
    class Meta:
        model = Product
        fields = ['id','price', 'sex', 'name','sizes'] 


class OrderSerializer(serializers.ModelSerializer):
    user_id = CustomerSerializer()
    store_id = StoreSerializer()
    class Meta:
        model = Order
        fields = ['total_price','order_date','delivery_date','delivery_status','is_restock','rewards_earned', 'user_id', 'store_id']



