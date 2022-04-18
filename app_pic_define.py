'''
   We are going to start interfacing with the database (adding Flask).
   
   We will separate the code that 
   1. defines the database
   2. initially populates the tables
   3. controls the forms for a user to add additional artists 

   That way all other code can import the definitions 
   Also that way we can run the "populate code" once 
   But can run the user-insert code over and over
'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
#from sqlalchemy import func

engine = create_engine('sqlite:///pic.db?check_same_thread=False')
#engine = create_engine('sqlite:///')
Base = declarative_base()

#####################################################################
# class to make a Poet
class Director(Base):
   __tablename__ = 'directors'
   
   id = Column(Integer, primary_key=True)
   lastName = Column(String)
   firstName = Column(String)
   country = Column(String)
   birthDate = Column(String)  # I've seen such old dates cause issues so I will stick to strings for now
   deathDate = Column(String)
   movies = relationship("Movie") # note relationship added to imports above
   
#######################################################################
  
class Movie(Base):
   __tablename__ = 'movies'
   
   id = Column(Integer, primary_key=True)
   title = Column(String)
   content = Column(String)
   director_id = Column(Integer, ForeignKey('directors.id'))
   # note: ForeignKey added to imports above
   # the argument of ForeignKey is a table.column  
   # note it's table name not class name

Base.metadata.create_all(engine)