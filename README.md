
# Phoenix Fire Alarm Project

The project consists of two Raspberry Pi, namely the main module and sensor module. The main module Raspberry Pi
version is on the branch `main` of the repository and the version for the sensor module is on the `SensorNode` branch.


**The main raspberry pi runs a server on Django(back-end) as well as the React server(front-end). The server has**
**built-in Django database, which stores the records of the sensor module's and displays the data on the front-end.**
**Main Raspberry Pi leaves two open ports within wireless local network which are dedicated to React [5173]**
**Django[8000].** 

#### Key Points


* **The Main  raspberry pi and sensor raspberry pi should be connected to the same wireless network in order to communicate.**


* **The server has to be configured and launched first. Afterward, launch as many sensor module raspberry pi as you want to exist in your system**


* **The system requires Internet Connection to Send Email to user**
### Contributors

1. #### Volodymyr Lysenko 
2. #### Arseniy Tokarev 
3. #### Sviatoslav Demchyuk 
5. #### Tabrea Leonard Fabian 
6. #### Jorim Hebbink 
7. ####  Luuk Alfing 


# Getting started Main Module

To make setup easy for you to get started with main module, here's a list of next steps.


## Clone the Project to your Pi

```
git clone https://gitlab.utwente.nl/computer-systems-project/2023-2024/student-projects/cs23-35/cs23-35-main.git
```
Alternatively, If something is wrong with `git clone` due to gitlab permissions, download zip of the project and transport it on your pi.

## Configure the project for ip of Raspberry Pi

- [ ] Tip: In order to find ip on your ip use `ifconfig`
### Config Django settings file
#### Change `'127.0.0.1'` in `ip = ` to your `ip = 'your Ip Here'`

```
sudo nano cs23-35-main/PhoenixMain/PhoenixMain/settings.py 
```
### Config the config file for React
#### Change `'127.0.0.1'` in `ipAddress = ` to your `ipAddress = "your Ip Here"`

```
sudo nano cs23-35-main/frontend/src/config.ts 
```


# Set up of Python Virtual Environment
If for some purpose you want to have a server on your machine and communicate only with sensor module you can set up on windows as well.
### Windows

```
cd .\cs23-35-main\
py -m venv myvenv
```
### Linux/MacOs

```
cd cs23-35-main
python -m venv myvenv
```

## Activate the environment and install the requirements

### Windows

```
.\myvenv\Scripts\activate
```

### Linux/MacOs

```
source myvenv/bin/activate
```

### After launch your console should look like this
```
(myvenv) PS G:\python\cs23-35-main> _
```

### Install requirements
```
pip install -r requirements.txt
```


# Setup of the project

### Apply django migrations

- [ ] Go to the directory PhoenixMain
- [ ] Make migrations and Migrate

#### For windows use `[python]` instead of [python3]
```
cd PhoenixMain
python3 manage.py makemigrations
python3 manage.py migrate
```
## Create a user for yourself
In the directory `cs23-35-main/PhoenixMain`

**NOTE: Please use Real Mail, as we have Two-Factor Authentication in our Project**

```
python3 manage.py createsuperuser
```


## Run the server
In the directory `cs23-35-main/PhoenixMain`
```
python3 manage.py runserver 0.0.0.0:8000
```

# Install the Nodejs
**Open separate terminal and run everything withouth the created virtual environment**
### Linux/MacOs
``` 
sudo apt update
sudo apt install nodejs
sudo apt install npm
```

### Windows
Install and set up from [official website](https://nodejs.org/en/download)

## Install the requirements for Nodejs

```
cd cs23-35-main/frontend/
npm install
```

## Run the React server

```
cd cs23-35-main/frontend/     #If not here Already
npm run dev --host
```

## Test and Deploy

All set up you can view and login with your credentials from any computer connected to the same network
* The project's website and main functionality go to link `**'ip_of_raspberry:5173`**
* The path for the database  if you want to check some of our models **`'ip_of_raspberry:8000/admin`**
* The system requires internet connection to send email to user


# The sensor module Raspberry PI
s
## Setup of the sensor module
#### **After the launch of the sensor module, they will communicate automatically and the room named `Undefined` will be added to fronted**

## Launch
Please use the readme on the branch `SensorNode` or use the [following link](https://gitlab.utwente.nl/computer-systems-project/2023-2024/student-projects/cs23-35/cs23-35-main/-/tree/SensorNode?ref_type=heads)

# Connect to the cloud (Microsoft Azure)
In order to connect to the cloud a Microsoft Azure account is needed - this can be done here https://azure.microsoft.com/ It is recommended to use an utwente email address in order to have some free credit as a student

Configure a subscription for you account
* Type 'Subscriptions' in the search field
* Click on '+ Add'
* Create a subscription, [TIP]: If you used an utwente email address you can chose the Azure for Students subscription

## Configuration of the server and SQL Database
You can find a good video tutorial here: https://www.youtube.com/watch?v=6joGkZMVX4o&t=369s

Text description
* Go to the top-left list icon and click it, select (+ Create a resource)
* Type 'SQL Database' in the search field and click on 'Create SQL Database'
* Select a subscription and a resource-group, in case you do not have a resource-group click 'Create new' and add a new resource group


## Creation of SQL TABLES
It is recommended to manage you SQL Database from the Azure Data Studio which can be downloaded here: https://azure.microsoft.com/en-us/products/data-studio
However, you can also run the queries from the web interface by going to the SQL Database and clicking on the 'Query editor (preview)' tab,
afterward enter your SQL Account Credentials. In any case, it is necessary to run the following queries in order to create the tables where
the local models entries will be inserted whenever SYNC operations are perfromed.

Run the following queries:
```
CREATE TABLE log (
    log_entry VARCHAR(MAX)
);
```


## Configuration of the storage account and blob container
You can find a video tutorial on the following link: https://www.youtube.com/watch?v=M_1R0ZOlP-w&t=240s

## Set up SYNC Thread
Whenever you run the project if you want to enable the cloud synchronisation services you need to open a new terminal, enter
the virtual environment, ```cd PhoenixMan``` and run in parallel the command ```python manage.py sfdafdsasfsadfds```

[TIP] If your machine will get another IP then the one that was configured in the Networks section when the SQL Database
was created a login error will occur. To fix that, go to the SQL Database, click 'Query editor (preview)' and try to log in with the SQL Account credentials,
If an error like unauthorized IP appears, just click on 'Update SQL server firewall rules'


## Manual SYNC
By default, whenever an error occurs the models and videos will be SYNCED with the cloud DB.

However, a manual SYNC is always possible from the terminal. Just enter the virtual environment, ```cd PhoenixMain``` and
run ```python manage.py sync_all_apps``` This command will Sync all videos and modals from the local DB to the cloud DB






























