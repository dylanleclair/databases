from django.contrib import admin

# Register your models here.
from .models import Question, User

admin.site.register(Question)
admin.site.register(User)