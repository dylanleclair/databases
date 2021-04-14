# databases

The term project for CPSC 471, the database management systems course at UofC. 

This project uses a SQLite database so that we can coordinate it with the repo of the project. 

If you are completely new to Django / Web Dev, I would recommend following the tutorial at the Django documentation to see how it all fits together. 

Otherwise, there is a vast amount of inline documentation. 

# Quickstart guide :rocket:

## Install some dependencies

To run our project, you will need Python - it was developed on Python 3.8. 

- Install django: `python -m pip install Django` 
- Install django REST framework: `pip install djangorestframework` and `pip install markdown`

Clone this repository to your computer.

To run the server locally, navigate to `realbeast/mysite` folder from the top repository directory, and run: 

`python manage.py runserver`

Then, you can open up http://127.0.0.1:8000/ in your browser - welcome to our website! :rocket:

## Using the quickstart

Only registered users can access their cart and place orders.

Sign into admin by navigating to the login page, enter:

- Username: `admin`
- Password: `12345`

From here, you can either do some shopping, update item information and more. The bulk of our time was spent getting our API operational, so the front-end isn't feature complete just yet. 

If you instead want the experience from a customer's point of view, register at the bottom of the homepage. 

# Our REST API :whale2:

Our Postman API is also included on our github - open the `RealbeastAPI.postman_collection.json` file in Postman, and you are set! :rocket:

The documentation for everything involved with that is accessible through Postman. 

All you need to do is boot up the local server as instructed above, and all of the requests in it should work flawlessly. :tada:

Try not to delete the admin user though.. This could cause some problems!

# To do list (web interface) :zap:
- creating base HTML documents for pages (with navbar) that we can extend to make more pages easier :heavy_check_mark: (See realbeast/templates/base.html)
- add user registration, sign in and account management pages :heavy_check_mark:
- add store page and product view pages :heavy_check_mark:
- added skeleton for filtering store (needs to be made functional) :arrows_counterclockwise:
- added skeleton for updating product information (quantities, description, titles, etc) :arrows_counterclockwise:
- implement Django REST to get desired API functionality (see Our REST API) :heavy_check_mark:


#### Notes to self (django stuff)

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

