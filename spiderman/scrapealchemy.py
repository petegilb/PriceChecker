# Our Own Library #

# --- Imports --- #
import scrapy
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

import QuoteItem

# --- Custom Object --- #

def getTypes(parseOutput):
    fields = {}
    for key, val in parseOutput.items():
        valType = String # Default
        # TODO - Code that checks the value and ascertains the type
        fields[key] = valType
    return fields

def getColumns(table):
    # columns = [key for key,val in table.__dict__.items() if not key.startswith('_')]
    columns = [column.key for column in table.__table__.columns]
    return columns

# Our Library Class
class Library:

    # Constructor
    def __init__(self, engine, base):
        self.engine = engine
        self.base = base
        self.tables = {}

    # Creates all of the tables for this Library's base on the engine
    def create_all_tables(self):
        self.base.metadata.create_all(self.engine)

    def create_table(self, name, fields):

        tablename = name.lower() + 's'

        # Creating a Base Class
        class TempClassName(self.base):
            __tablename__ = tablename
            id = Column(String, primary_key=True)      

        # Changing the temp name to the actual name
        table = TempClassName
        table.__name__ = name

        for key, val in fields.items():
            setattr(table, key, Column(String)) # Temp

        # def toString(self):
        #         return "<{}(id={}, name='{}'>".format(name,self.id, self.get_name())     

        self.tables[name] = table

        # Return this new class
        return table

    # pass in a sqlalchemy table class
    def add_table(self, table):
        self.tables[table.__tablename__] = table

    # Scrapy.Item as an argument
    def insertItem(self, table, item):
        assert isinstance(item, scrapy.Item)
        Session = sessionmaker(bind=self.engine)
        session = Session()
        # data = table() 
        data = self.tables[table]()
        for key, val in item.items():
            # print('Key:',key,'Value:',val)
            # data[key] = val
            print(data)

        session.commit()


    # Multiple arguments
    # def insertItem(*item):
    #     pass