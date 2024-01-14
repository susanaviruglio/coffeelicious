# Coffeelicious
## Full Stack Frameworks with Django Milestone Project by Susana Viruglio

Welcome to Coffeelicious, where we know that life is too short for a bad coffee and
dive into tastiest coffees from around the world. This Coffeeshop has been built by using a full stack framework with Django, your journey starts here.

<img src="static/images/presentation.png">


### External User Goals

- Easily find coffee or similar drink through the coffee shop's products.

- Provide categories and filter products to help users find specific type of coffee, tea, etc.

- Detail information about each item.

- Users may wish to create an account to improve their experience by allowing registration.

- Provide a shopping cart visible and easy to access; easy to delete, to add or modify.


### Site Owner's Goals

- To maximize profitability by creating a web which makes the website more attractive for customers.

### Potential Features To Include

- User registration and profile.

- A coffee and tea catalogue with images and well organized.

- Product search and filter to help users to find easily specific products.

- Shopping cart.

- Promotions and discounts.

## UX AIMS

- As a shopper I would like to be able to view a list of coffee products, so I can select some to purchase.

- Clicking on an individual product, so I am able to view product details and identify the price, product description, product rating, product image.

- A navigation menu that allows users to identify deals or special offers.

- Create an user account which allows to make purchases.




1. **How can create an user account?** I would like to create an account and log in so I am able to save all my bank details the next time I wish to do another purchase.

2. **I would like to buy coffee but I do not want to create an account** It is possible to make purchases as a guest in this store.

3. **Where can I found special offers?** In the navigation menu allows users to be able to see easily offers or special deals.

4. **Where am I able to see how much I spend in total?** A real shopping indicator that allows users to view total amount of the purchase at any time ir order to avoid spending too much.

5. **I have forgotten my password** Reset the users'password if the have forgotten.


## DESIGN EVOLUTION


## TESTING 

**Allauth Directory Templates**

I created a directory templates allauth because I wanted to customize the allauth templates in my own allauth, so this ensures that my templates take precedence over the built ones.
This gives a copy of every single Allauth template.
I tried to copy everything that I needed with the command cp -r which means to copy recursively
../ to go up one level from where we are right now.
	cp -r ../.pip-modules/lib/python3.9.17/site-packages/allauth/templates/* ./templates/allauth
so this link did not work so I typed : find / -type d -name "allauth" and I found the real directory for gitpod
	cp -r /workspace/.pip-modules/lib/python3.9/site-packages/allauth/templates/* ./templates/allauth/
**Bad Request** 

When I was working on my Profile app, I encountered with Bad Request error:

"Bad Request: /checkout/wh/ [13/Jan/2024 11:29:33] "POST /checkout/wh/ HTTP/1.1" 400 0".

I found out that normally it indicates that the server did not understand the request. I realised that I forgot to import settings.py on my webhook_handler.py file.

**Template Does Not Exist**

I received this error message when I was trying to access checkout.html file:
"TemplateDoesNotExist at /checkout/includes/toasts/warning.html"

It was another typo in my spellings because I forgot an in s in warnings.html

**Module Not Found**

When I was trying to run the server I encountered wit this error in the terminal:

"ModuleNotFoundError: No module named 'checkoutcrispy_forms'"

I was checking everywhere for the error, but it was a typo in my settings.py I forgot to add a comma in my intalled_apps.

**Type Error**

I encountered 'TypeError' at line 48 of the adjust_shopping_bag function in the views.py file. To resolve the issue I had to review carefully the views.py specifically in the line 48.

I looked for the line where I was using square brackets to access an item, like bag.pop[item_id] instead of using parentheses "bag.pop(item_id)".

## DEPLOYMENT

### Github

This project is deployed using GitHub pages using the following process:

**Deploying a GitHub Repository via GitHub Pages**

1. In your Repository section, select the Repository you wish to deploy.
2. In the top horizontal Menu, locate and click the Settings link.
3. Inside the Setting page, around halfway down locate the GitHub Pages Section.
4. Under Source, select the None tab and change it to Master and click Save.
5. Finally once the page resets scroll back down to the GitHub Pages Section to see the following message *"Your site is ready to be published at (Link to the GitHub Page Web Address)"*. It can take time for the link to open your project initially, so please don't be worried if it down not load immediately.

**Forking the Github Repository**

You can fork a GitHub Repository to make a copy of the original repository to view or make changes without it affecting the original repository.

- Find the GitHub repository.
- At the top of the page to the right, under your account, click the Fork button.
- You will now have a copy of the repository in your GitHub account.
  
**Making a Local Clone**

1. Find the GitHub Repository.
2. Click the Code button
3. Copy the link shown.
4. In Gitpod, change the directory to the location you would like the cloned directory to be located.
5. Type git clone, and paste the link you copied in step 
6. Press Enter to have the local clone created.

[Web link once deployed](LINK)
### HEROKU and ELEPHANTSQL
Deploying a Python application on Heroku involves several steps. Here's a general guide:
If you don't have a Heroku account, sign up for one at Heroku's website.
1. Create an account with ElephantSQL
2. Authorise ElephantSQL with your selected GitHub account
3. In the Create new team form:
   - Add a team name (your own name is fine)
   - Read and agree to the Terms of Service
   - Select Yes for GDPR
   - Provide your email address
   - Click “Create Team”
4. Your account is successfully created!
Create a database
5. Click “Create New Instance”
6. Set up your plan (give a name, select the tiny turtle plan and Irish region)
7. Select data center near you (Ireland)
8. Then, click Review
9. Check your details are correct and then click “Create instance”
10. Return to the ElephantSQL dashboard and click on the database instance name for this project
11. In the URL section, clicking the copy icon will copy the database URL to your clipboard
12. Leave this tab open, we will come back here later

Before we can build our application on Heroku, we need to create a few files that Heroku will need to run our application:

- A requirements.txt file which contains a list of the Python dependencies that our project needs in order to run successfully.

- A Procfile which contains the start command to run the project.
**Process**
1. Generate the requirements.txt file with the following command in the terminal. After you run this command a new file called requirements.txt should appear in your root directory

 pip freeze --local > requirements.txt

2. Heroku requires a Procfile containing a command to run your program. Inside the root directory of your project create the new file. It must be called Procfile with a capital P, otherwise Heroku won’t recognise it

3. Inside the file, add the following command:

 web: python run.py

4. Open your init file

5. Add an if statement before the line setting the SLQALCHEMY_DATABASE_URI and, in the else, set the value to reference a new variable, DATABASE_URL.

 app = Flask(__name__)
 app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

 if os.environ.get("DEVELOPMENT") == "True":
     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
 else:
     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

6. To ensure that SQLAlchemy can also read our external database, its URL needs to start with “postgresql://”, but we should not change this in the environment variable. Instead, we’ll make an addition to our else statement from the previous step to adjust our DATABASE_URL in case it starts with postgres://:

 if os.environ.get("DEVELOPMENT") == "True":
     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
 else:
     uri = os.environ.get("DATABASE_URL")
     if uri.startswith("postgres://"):
         uri = uri.replace("postgres://", "postgresql://", 1)
     app.config["SQLALCHEMY_DATABASE_URI"] = uri
7. Save all your files and then add, commit and push your changes to GitHub

**Heroku process**

Now that you have your database and code in your IDE configured, we will add it to a Heroku app using a new environment variable (Config Var) called DATABASE_URL. Then our Heroku app will be able to connect to the external database.

1. Log into Heroku.com and click “New” and then “Create a new app”
2. Choose a unique name for your app, select the region closest to you and click “Create app”
3. Go to the Settings tab of your new app
4. Click Reveal Config Vars
5. Return to your ElephantSQL tab and copy your database URL
6. Back on Heroku, add a Config Var called DATABASE_URL and paste your ElephantSQL database URL in as the value. Make sure you click “Add”
7. Add each of your other environment variables except DEVELOPMENT and DB_URL from the env.py file as a Config Var. The result should look something like this:
<img src= bookmanager/static/images/heroku-env-vars.png>

**Deploy the app**

1. Navigate to the “Deploy” tab of your app
2. In the Deployment method section, select “Connect to GitHub”
3. Search for your repo and click Connect
4. Optional: You can click Enable Automatic Deploys in case you make any further changes to the project. This will trigger any time code is pushed to your GitHub repository.
5. As we already have all our changes pushed to GitHub, we will use the Manual deploy section and click Deploy Branch. This will start the build process. 
6. Now, we have our project in place, and we have an empty database ready for use. As you may remember from our local development, we still need to add our tables to our database. To do this, we can click the “More” button and select “Run console”.
7. Type python3 into the console and click Run
8. This opens the Python terminal, in the same way as it would if we typed python3 into the terminal within our IDE. Let’s now create the tables with the commands we used before.
9. Exit the Python terminal, by typing exit() and hitting enter, and close the console. Our Heroku database should now have the tables and columns created from our models.py file.

## HTML AND CSS VALIDATOR
### HTML


### CSS


### JAVASCRIPT




### PYTHON


### LIGHTHOUSE


## CREDITS
All the code that I have used to create this website was taken from Code Institute learning platform and from the next following sources:

[BOOTSTRAP](https://getbootstrap.com/docs/5.1/getting-started/introduction/)
HTML 

[UNPLUSH](https://unsplash.com/photos/brown-and-blue-plastic-pack-mSjTAV7JuV4)
Coffee images were taken from this free Unplush but I modified the logo for each type of coffee.

[LOGO MAKER](https://www.adobe.com/express/create/logo)
Logo design for each coffee were taken from this free source and I pasted on the coffee bag.

[STARBUCKS](https://www.starbucks.co.uk/menu/at-home/whole-bean)
Coffee information and product structure and category names.

[TEXTFIXER](https://www.textfixer.com/tools/paragraph-to-lines.php)
Paragraph converter for the json file.

[W3SCHOOL](https://www.w3schools.com/css/css3_shadows_box.asp)
Box shadow effect for the product images

## EXTRA INFORMATION 

