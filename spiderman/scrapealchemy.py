# Our Own Library #

# --- Imports --- #
import scrapy
import sqlalchemy
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Sequence

# import QuoteItem

# --- Custom Object --- #

def getTypes(parseOutput):
    fields = {}
    for key, val in parseOutput.items():    
        valType = getType(key, val)    
        # TODO - Code that checks the value and ascertains the type        
        fields[key] = valType
    return fields

def getType(key, val):
    valType = String # Default
    if isinstance(val, str):
        print('String')
        valType = String
    elif isinstance(val, int):
        print('Integer')
        valType = Integer
    elif isinstance(val, float):
        print('Float')
        valType = Float
    elif isinstance(val, list):
        print('Sequence')
        if len(val) > 0:
            # valType = [getType(key,val[0]),Sequence(key)] # Not Supporting Sequences
            valType = String
        else:
            print('Can\'t infer type for Sequence! Assuming sqlalchemy.String!')
            # valType = [String,Sequence] # Not Supporting Sequences
            valType = String
    else:
        print('Can\'t infer type! Assuming sqlalchemy.String!')
    return valType

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

        # Creating a Base Class - (Doesn't Support Sequences)
        class TempClassName(self.base):
            __tablename__ = tablename
            id = Column(Integer, primary_key=True)            

            def __repr__(self):
                fields = [key for key in getColumns(self) if key != 'id']
                formatStr = "<{}(" + ','.join([key + '={}' for key in fields]) + ")>"
                formatArgs = [name] + [getattr(self, key) for key in fields] # name == self.__name__
                return formatStr.format(*formatArgs)

        # Changing the temp name to the actual name
        table = TempClassName
        table.__name__ = name

        for key, val in fields.items():
            if isinstance(val, list):
                setattr(table, key, Column(*val))
            else:
                setattr(table, key, Column(val))

        # formatStr = "<{}(" + ','.join([key + '={}' for key in getColumns(table)]) + ")>"
        # formatArgs = [name] + [getattr(table, key) for key in getColumns(table)]
                
        # print('Format Strings:',formatStr)
        # print('Format Arguments:',formatArgs)
        # print('ID:',table.id)
        # print(formatStr.format(*formatArgs))

        # def toString(self):
        #     formatStr = "<{}(" + ','.join([key + '={}' for key in getColumns(table)]) + ")>"
        #     formatArgs = [name] + [getattr(self, key) for key in getColumns(table)] # name == table.__tablename__
        #     return formatStr.format(*formatArgs)

        # table.__repr__ = toString

        # --- Tests --- #

        # temp = TempClassName()
        # print('Temp Table:',temp)

        # ------------- #

        self.tables[tablename] = table

        # Return this new class
        return table

    # pass in a sqlalchemy table class
    def add_table(self, table):
        self.tables[table.__tablename__] = table

    def insert(self, tableClass, obj):
        if isinstance(obj, scrapy.Item):
            self.insertItem(tableClass, obj)
        elif isinstance(obj, dict):
            self.insertDict(tableClass, obj)
        else:
            print('Couldn\'t Insert Object:',obj,'.\nIt was not a valid type!')

    # Scrapy.Item and sqlalchemy class as arguments
    def insertItem(self, tableClass, item):
        assert isinstance(item, scrapy.Item)
        dictionary = item.items()
        self.insertDict(tableClass, dictionary)

    # Scrapy.Item and sqlalchemy class as arguments
    def insertDict(self, tableClass, obj):
        assert isinstance(obj, dict)
        Session = sessionmaker(bind=self.engine)
        session = Session()
        table = tableClass() 
        print(tableClass)
        # table = self.tables[table]()
        for key, val in obj.items():
            # print('Key:',key,'Value:',val)
            # data[key] = val # Doesn't Work
            if isinstance(val, list):
                setattr(table, key, ','.join(val))
            else:
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
