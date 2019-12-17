# Our Own Library #

# --- Imports --- #
import scrapy
import sqlalchemy
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

<<<<<<< HEAD
# import QuoteItem

=======
>>>>>>> 6cf3fdd679c6de6fd1d7fd552ad12648f7ce23e1
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
<<<<<<< HEAD
            id = Column(Integer, primary_key=True)      

            def __repr__(self):
                fields = [key for key in getColumns(self) if key != 'id']
                formatStr = "<{}(" + ','.join([key + '={}' for key in fields]) + ")>"
                formatArgs = [name] + [getattr(self, key) for key in fields] # name == self.__name__
                return formatStr.format(*formatArgs)
=======
            id = Column(String, primary_key=True)
>>>>>>> 6cf3fdd679c6de6fd1d7fd552ad12648f7ce23e1

        # Changing the temp name to the actual name
        table = TempClassName
        table.__name__ = name

        for key, val in fields.items():
            setattr(table, key, Column(String)) # Temp

        # formatStr = "<{}(" + ','.join([key + '={}' for key in getColumns(table)]) + ")>"
        # formatArgs = [name] + [getattr(table, key) for key in getColumns(table)]
                
        # print('Format Strings:',formatStr)
        # print('Format Arguments:',formatArgs)
        # print('ID:',table.id)
        # print(formatStr.format(*formatArgs))

        # def toString(self):
<<<<<<< HEAD
        #     formatStr = "<{}(" + ','.join([key + '={}' for key in getColumns(table)]) + ")>"
        #     formatArgs = [name] + [getattr(self, key) for key in getColumns(table)] # name == table.__tablename__
        #     return formatStr.format(*formatArgs)

        # table.__repr__ = toString

        # --- Tests --- #

        # temp = TempClassName()
        # print('Temp Table:',temp)

        # ------------- #
=======
        #         return "<{}(id={}, name='{}'>".format(name,self.id, self.get_name())
>>>>>>> 6cf3fdd679c6de6fd1d7fd552ad12648f7ce23e1

        self.tables[tablename] = table

        # Return this new class
        return table

    # pass in a sqlalchemy table class
    def add_table(self, table):
        self.tables[table.__tablename__] = table

    # Scrapy.Item and sqlalchemy class as arguments
    def insertItem(self, tableClass, item):
        assert isinstance(item, scrapy.Item)
        Session = sessionmaker(bind=self.engine)
        session = Session()
<<<<<<< HEAD
        table = tableClass() 
        print(tableClass)
        # table = self.tables[table]()
=======
        # data = table()
        data = self.tables[table]()
>>>>>>> 6cf3fdd679c6de6fd1d7fd552ad12648f7ce23e1
        for key, val in item.items():
            # print('Key:',key,'Value:',val)
            # data[key] = val # Doesn't Work
            setattr(table, key, val)
            
        print('Table:',table)
        print(getColumns(table))
        session.add(table)

        # print(tableClass)
        # results = session.query(tableClass).all()
        # print(results)

        session.commit()


    # Multiple arguments
    # def insertItem(*item):
    #     pass
