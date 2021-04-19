from rest_framework import routers

class RealbeastAPI(routers.APIRootView):
    '''
    Welcome to our API! 

    Our API is browsable, but also responds to HTTP requests like any other API would. 

    To use it in Postman, you will need to set up authentication - use a basic auth type with:
    
    - Username: `stellaellaolla`
    
    - Password: `12345`

    To get you started with some examples:

    ... add examples here!


    You can even access it through the webpage here, if you login with the above credentials.
    '''
    pass

class DocumentedRouter(routers.DefaultRouter):
    APIRootView = RealbeastAPI