# databases
databases project for school

This project will connect to a MySQL server running on localhost, with:
- username: admin
- password: password

(maybe move over to noSQL so we can coordinate it?)

and runs the web app. 

I recommend following the tutorial at the Django documentation to see how it all fits together. There is a good amount of inline documentation as well. 

### Handy commands

#### Getting started

I'd recommend you go through at least a bit of the tutorial at the Django documentation.

https://docs.djangoproject.com/en/3.1/intro/tutorial01/

#### Changing models in the database

To change items in the database, you will first want to change the model (realbeast/models.py). 

After making your changes, stage them with: 

`python manage.py makemigrations`

Then call:

`python manage.py migrate`

to carry the changes you made in the model into the server.

#### Seeding the database

This is done with fixtures. 

Create a JSON file in `realbeast/fixtures` with the name of the model you want to seed data for. 

For example `Products.json` is used to seed data into the Projects table. 

Then call `python manage.py dumpdata realbeast.Product > ./realbeast/fixtures/Product.json` to make Django recognize it. 

Then, any time you update the values in Product.json, you can move them into the database with  `python manage.py loaddata Product`

Evenutally, I want to set up something that can programmatically do this. :) 

#### Currently:

I'm working on managing sign ins and authentications so that I can start to add cart / shopping functionality down the line. 

The resource I'm following is:
https://learndjango.com/tutorials/django-login-and-logout-tutorial

https://docs.djangoproject.com/en/3.1/ref/templates/language/

#### Goals for future
- creating base HTML documents for pages (with navbar) that we can extend to make more pages easier :heavy_check_mark: (See realbeast/templates/base.html)
- stylizing login page (goes hand in hand with the above)
    - ready to go, just needs polishing:heavy_check_mark:
- creating an account management page (also goes hand in hand with first) :arrows_counterclockwise:
    - drafted :heavy_check_mark:
    - add ability to update data 
- adding form functionality to product page so that filters can be applied for: :arrows_counterclockwise:
    - sizes
    - colours
    - product types
    - sex  
- add previews of quantity (per store) for each product :heavy_check_mark:
- implement Django REST to get us an API (due for the 25th) :arrows_counterclockwise:

# Our REST API

Our API can be accessed through HTML or through Postman. 

To modify data in postman, you will have to add basic authentication. 

A sample user you may use is: 

Username: `stellaellaolla`
Password: `12345`

Documentation for our REST API can be found at localhost:8000/api.


### old

To open the solution for this project, navigate to RealBeast > RealBeast.csproj and double click. It will open up in Visual Studio.

To create an instance of the database on your computer, open Tools > NuGet Package Manager > Package Manager Console, and run `Update-Database`.

From there, you can experiment with the data. There is next to no functionality yet but the groundwork is just about done!
