# dm_python
Decision Making Project - Harokopio University


https://docs.google.com/document/d/1m4vlDOGy09i7b5G351CNAZbyxmgB-oSxVaTrAmuBGpw/edit

pip install geopandas mysql-connector-python matplotlib

pip install geoplot

sudo /opt/lampp/lampp start



======================================================

PROJECT EXPLANATION  (video link : https://www.youtube.com/watch?v=rnpuoQpnbPg )

======================================================

Files examplation:

base.py --> This is the main .py file that makes some basic api calls, saving info to the database and calls every other .py file to execute all the different functionalities of the project 

database_init.py --> This file manages the database tables.Drops every table in each execution to clear the database data, and recreates the tables to be ready to be called

db_connect.py --> This file is responsible for the connectivity throw the database. We call import this file in each other .py file to be able to accomplish connection and execute queries to the database

generateRandomLatLOn.py --> This function generates synthetic Lat Lot points. We maded it so can generate points only in the region of the coutry France for simplicity reasons.

geneticAlgo.py --> This file takes info from files album.price.csv & user_money_rates.csv from the folder csv, and generates a list of albums that each user can buy in order to maximise his desires and at the same time stay in budget

geoplotExec.py --> This file exports a plot with a france map on it. It renders the different favorite song points of each user and generates some general conclusions

helperAI.py --> This file uses ChatGPT open api to generate random user names so they can be used as a sample to our testing functions.We managed to use it just one time because of api calls limitation. We saved the results and we made sure that we wont delete the table storing them in each new execution of the project.The function works, but needs an api key from a premium account.

lastfm_api --> This file executes api calls to lastfm's api to retrive some additional info that we considered usefull in our differect execution scenarios

manageData.pu --> This file executes some basic functionalities to the database in order to increase the quality of our managed data on our databse

nameFiltering.pu --> This file executes a filtering process in order to clear duplicates on the results that we got from the Chatgpt username generator.

recommend.py --> This file recommends songs to users based on their barabasi model neighbors

arima.py --> This file manages the different data from the file file_series.csv and generates predictions about the final prices



