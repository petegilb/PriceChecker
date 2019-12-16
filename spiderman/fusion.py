import scrapy
import sqlalchemy
from sqlalchemy import create_engine
import subprocess #this is for running the code
#import ourLibrary
#this is gonna be the file where you can use/class and fuse both scrapy and sqlalchemy

def fuse():
    #creates a json file called data.json that is the output of the information we scraped
    return_code = subprocess.call("scrapy crawl quotes -o data.json",shell=True)
    #ourLibrary.create_table() #create the table and then

fuse()
