from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    return HttpResponseRedirect(reverse('realbeast:index'))