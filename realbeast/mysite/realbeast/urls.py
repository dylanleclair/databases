from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # this code will:
    # match a path with /realbeast/<integer> (ex: localhost:8000/realbeast/1)
    # it will then call the function with the name 'detail' from the module views.detail (see views)
    # this function returns and HTTP request, which we can customize to use
    # a template (see templates/realbeast) to create a custom HTML page using the object 
    # we retreive in the views.detail function. 

    #in summary, we want to query the database using information from the path
    #to serve an HTTP GET request by providing a webpage to the client requesting it

    # this can be plain text, or you can load python data into a dictionary as a context
    # and pass this to the template page, which unpacks and uses the python data 
    # in the http response sent to the user (user is a browser)

    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]