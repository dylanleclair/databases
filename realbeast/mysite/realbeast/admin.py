from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.
from .models import *

admin.site.register(Profile)
admin.site.register(PaymentInfo)
admin.site.register(Store)
admin.site.register(WorksAt)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Product)
admin.site.register(Details)
admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(ProductType)
admin.site.register(Color)
admin.site.register(Contains)


#admin.site.register(User, Profile)