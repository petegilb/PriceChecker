import scrapy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import subprocess #this is for running the code
import scrapealchemy
from scrapealchemy import Library
import json
#this is gonna be the file where you can use/class and fuse both scrapy and sqlalchemy

def fuse():
    #creates a json file called data.json that is the output of the information we scraped
    #return_code = subprocess.call("scrapy crawl quotes -o data.json",shell=True)
    #ourLibrary.create_table() #create the table and then
    with open('data.json') as x:
        data = json.load(x)
    #print(data[0])
    library = scrapealchemy.Library
    engine = create_engine('sqlite:///:memory:', echo=True)
    #print(engine, sqlalchemy.__version__)
    base = declarative_base()
    greatLibrary = Library(engine,base)
    library.create_table(greatLibrary, 'test',scrapealchemy.getTypes(data[0]))
    greatLibrary.create_all_tables()
    #generated all of the tables for the data
    #as of now the user has to create their own scrapy spider to scrape the website but it should automatically be placed into a table

fuse()
