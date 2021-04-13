# databases
databases project for school

This project uses a SQLite database so that we can coordinate it with the repo of the project. 

I recommend following the tutorial at the Django documentation to see how it all fits together. There is a good amount of inline documentation as well. 

# Quickstart guide

Clone this repository to your computer.

To run the server locally, navigate to `realbeast/mysite` folder from the top repository directory, and run: 

`python manage.py runserver`

Then, you can open up http://127.0.0.1:8000/ in your browser - welcome to our website!

A browsable API is available at http://127.0.0.1:8000/api

## Using the quickstart

Only registered users can access their cart and place orders.

Sign into admin by navigating to the login page, enter:

- Username: `admin`
- Password: `12345`

From here, you can either do some shopping, update item information, place restock orders and more. 

# Our REST API

Our Postman API is also included on our github - open the `RealbeastAPI.postman_collection.json` file in Postman, and you are set!

The documentation for everything involved with that is accessible through Postman. 

# To do list (web interface)
- creating base HTML documents for pages (with navbar) that we can extend to make more pages easier :heavy_check_mark: (See realbeast/templates/base.html)
- add user registration, sign in and account management pages :heavy_check_mark:
- add store page and product view pages :heavy_check_mark:
- added skeleton for filtering store (needs to be made functional) :arrows_counterclockwise:
- added skeleton for updating product information (quantities, description, titles, etc) :arrows_counterclockwise:
- implement Django REST to get desired API functionality (see endpoints) :arrows_counterclockwise:


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

Evenutally, I want to set up something that can programmatically do this. :) 

