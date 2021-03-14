from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User
# Create your views here.

def index(request):
    user_list = User.objects.all()[:5]
    template = loader.get_template('realbeast/realindex.html')
    context = {
        'user_list':user_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)