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

class SimpleStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['location']


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

        online = Store.objects.get(location="Online")
        # Create the user's cart
        Order.objects.create(user_id=user,store_id=online, delivery_status="Cart")

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


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'sex', 'name'] 

class ProductSerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    product_types = ProductTypeSerializer(many=True)
    colors = ProductColorSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id','price', 'sex', 'name', 'description','caption','img_name', 'brands','product_types','colors'] 

    # Used to create a new product
    def create(self, validated_data):
        
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

class SimpleSizeSerializer(serializers.ModelSerializer):
    # Refer to the location of the store associated with this size object
    location = serializers.CharField(source='store_id.location')
    class Meta:
        model = Size
        fields=['location','product_id','size', 'quantity']

    def create(self, validated_data):
        # update product information

        product_data = validated_data.get('product_id', None) # see simple product serializer
        store = validated_data.get('store_id', None) # see simple store serializer
        size = validated_data.get('size',None)
        quantity = validated_data.get('quantity', None)

        # Do some extra work to get the store from the location
        store_data = Store.objects.get(location=store["location"])
        instance = Size.objects.create(product_id=product_data, store_id=store_data, size=size, quantity=quantity)
        instance.save()

        return instance

   # code for updating a product
    def update(self, instance, validated_data):

        # instance is the object being updated
        instance.product_id = validated_data.get('product_id', instance.product_id) # see simple product serializer
        instance.store_id = validated_data.get('store_id', instance.store_id) # see simple store serializer
        instance.size = validated_data.get('size',instance.size)
        instance.quantity = validated_data.get('quantity', instance.quantity)

        # update product information
        instance.save()

        return instance


class ContainsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contains
        fields=['id','product_id','quantity','size']

class OrderSerializer(serializers.ModelSerializer):
    location = serializers.CharField(source='store_id.location')
    username = serializers.CharField(source='user_id.username')
    contains = ContainsSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','username','location','delivery_status','contains','rewards_earned','total_price','order_date','delivery_date','is_restock']

    
    def create(self, validated_data):
        # create a new instance from the validated data
        
        return None