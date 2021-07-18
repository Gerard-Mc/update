# Deployment

## Local Deployment

Gitpod, an integrated development environment, was used to code this project. Github was used for version control and storing the project's files remotely.

To run this project you will need to perform the following steps.

### Install Technologies to Your Computer

[PIP](https://pip.pypa.io/en/stable/installing) to install the project's requirements.
[GIT](https://www.atlassian.com/git/tutorials/install-git) for cloning the project and version control.
[Python](https://www.python.org/download/releases/3.0/) to run the project. 

### Clone the Repository

You will need to clone the site's repository.
To do this,  enter `git clone https://github.com/Gerard-Mc/milestone_4.git` into your terminal.
After the repository is cloned, change IDE directory to the one created after cloning by typing `cd <path to project folder>` into yor terminal.
You will find more information on cloning repositories [here](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository)

### Create Accounts

The website requires a Stripe, Gmail, and AWS account.
You will find links to them below.
[Stripe](https://stripe.com/)
[Gmail](https://www.google.com/)
[AWS](https://aws.amazon.com/)

### Set up Environment Variables
* Create an env.py file in the root directory.
* If not already included in the .gitignore file, make sure to add it otherwise your environment files will be visible to the public.
* Paste the following code into the env.py file and input the values found in your Stripe account.
```
import os  
os.environ["DEVELOPMENT"] = "True"    
os.environ["SECRET_KEY"] = "<Your Secret Key>"
os.environ["STRIPE_PUBLIC_KEY"] = "<Your Stripe Public Key>"    
os.environ["STRIPE_SECRET_KEY"] = "<Your Stripe Secret Key>"    
os.environ["STRIPE_WH_SECRET"] = "<Your Stripe WH Secret Key>"    
```
More information on setting up Stripe keys can be found [here](https://stripe.com/docs).

### Install Required Packages

To install the required packages, input `pip3 install -r requirements.txt`
in your terminal.

### Create Database
* You will need to make migrations by inputting `python3 manage.py makemigrations` into your terminal.

* Migrate this data by inputting `python3 manage.py migrate` into your terminal.

### Create a Super User 

To access the website's admin to create objects, you will first have to create an admin account.
* Input `python3 manage.py createsuperuser` into your terminal.
* Follow the steps by inputting a username, email(optional), and a password.
* To open admin, you will need to open the website. To do this type `python3 manage.py runserver` in your terminal and an option to open the website should be available in your IDE.
* After you open the website, add `/admin` to the end of the websites URL to open Admin.
* Click categories and create 4 different categories ensuring all 4 names are used and used only once. You can input whatever you wish into the friendly name and price fields.
The database and website should now work as expected.

# Deployment
## Remote Deployment

### Set up an AWS account
Images for the website were stored remotely by using a S3 Bucket provided by AWS.
You will need to set up an AWS account, create a Bucket with public access, and input your credentials in the Heroku config vars section of the app's Heroku settings(explained later).
In the settings.py file provided in the repository, input the Bucket name and the region name like the example format below.
```
AWS_STORAGE_BUCKET_NAME = 'your bucket name'
AWS_S3_REGION_NAME = 'the region you choose'
```
The rest of the variables will be handled in the settings.py file included in the repository, and won't need a further configuration. After the Heroku app is created, they will need to be inputted as config vars. That will be shown in the coming Heroku section.

More information on creating and setting up Buckets can be found [here](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html)

### Create a Heroku App and Deploy
[Heroku](https://www.heroku.com/) was used to host this project. The steps needed to get the project up and running are provided below.

Create a Heroku account and create a new project app.
When prompted, choose the region that is closest to you.
When the app is created, go to the **resources** tab, search for the addon **Heroku Postgress**, and install it to your app.
Go to the **Settings** tab, click **Reveal Config Vars**, and input your environment variables in the below format.
```
AWS_ACCESS_KEY_ID : `<your AWS access key>`
DATABASE_URL: `<your database url>`
AWS_SECRET_ACCESS_KEY: `<your AWS secret access key>`
USE_AWS: `<True>`
SECRET_KEY: `<your secret key>`
EMAIL_HOST_PASS: `<your email password>`
EMAIL_HOST_USER: `<your email address>`
STRIPE_PUBLIC_KEY:	`<your stripe public key>`
STRIPE_SECRET_KEY:	`<your stripe secret key>`
STRIPE_WH_SECRET: `<your stripe wh key>`
```
The database URL in the environment variables is connected to the app in the settings.py file and won't need a further configuration.
```
DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
```


The requirements.txt and Procfile Heroku will need to run this project are included in the repository files and Heroku will use them in the build automatically.
For reference, they are provided below.
[Procfile](/workspace/milestone_4/Procfile)
[Requirements.txt](/workspace/milestone_4/requirements.txt)

Deploy on Heroku
* Go to **settings > config vars** and input the key **DISABLE_COLLECTSTATIC** and set it to **True** 
* Go to the **Deploy** tab in the Heroku dashboard.
* At **Deployment Method**, choose Github and then connect to your cloned repository.
* Choose **Automatic Deploy**, and click **Deploy Branch **.

Go back to the settings.py file in your IDE, and in the line `ALLOWED_HOSTS =`, add set it equal to your website's address in the format below.

`ALLOWED_HOSTS = ['example.herokuapp.com']`

* Push the changes to Github and go back to **Settings > Config Vars**, and remove **DISABLE_COLLECTSTATIC**.
* Redeploy the website in **Deploy > Deploy Branch** in the Heroku dashboard and the website should be up and running.

* Go to the terminal in Heroku and follow the instructions under the headings **Create Database** and **Create a Super User** in the Local deployment section, and the website should b up and running.

