from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from rest_framework import routers

def index(request):
    return HttpResponseRedirect(reverse('realbeast:index'))

