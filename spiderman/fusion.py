import scrapy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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

    test_data = [
        {'price': 2.25, 'year': 2019, 'description': 'A small example of how this works', 'tags': ['591','Alex','Peter','Code']}
    ]

    #print(data[0])
    library = scrapealchemy.Library
    engine = create_engine('sqlite:///:memory:', echo=True)
    #print(engine, sqlalchemy.__version__)
    base = declarative_base()
    greatLibrary = Library(engine,base)
    types = scrapealchemy.getTypes(data[0])
    # types = scrapealchemy.getTypes(test_data[0])
    print('Types:',types)
    test = library.create_table(greatLibrary, 'test', types)
    greatLibrary.create_all_tables()
    #generated all of the tables for the data
    #as of now the user has to create their own scrapy spider to scrape the website but it should automatically be placed into a table        

    # Inserting Into Table
    for datum in data:
        greatLibrary.insert(test,datum)

    # for datum in test_data:
    #     greatLibrary.insert(test,datum)

    # Querying
    Session = sessionmaker(bind=engine)
    session = Session()

    results = session.query(test).all()
    print(results)

    session.commit()



fuse()
