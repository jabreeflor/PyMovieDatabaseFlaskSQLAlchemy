# Defining a form for entering data to insert an artist 
# into our art database

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import InputRequired, Length

import app_pic_define as my_db

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=my_db.engine)
session = Session()

movie_list = session.query(my_db.Movie).all()
movie_choices = []
for item in movie_list:
   mylist=[]
   mylist.append(str(item.id))
   mylist.append("{}".format(item.title) )
   my_tuple = tuple(mylist)
   movie_choices.append(my_tuple)
#########################################################
# Class for inserting an director 
class Director_Form(FlaskForm):
   lastName = StringField("last name", 
   validators=[InputRequired(message="You must enter a last name"), 
   Length(min=2, max=60, message="Last Name length must be between 2 and 60 characters")])

   # for now we are requiring first and last name but that can cause issues  
   firstName = StringField("first name", 
   validators=[InputRequired(message="You must enter a first name"), 
   Length(min=2, max=60, message="First Name length must be between 2 and 60 characters")])
   
   country = StringField("Country", 
   validators=[InputRequired(message="You must enter a country"), 
   Length(min=2, max=60, message="Country length must be between 2 and 60 characters")])

   birthDate = StringField("Birth Date")

   deathDate = StringField("Death Date")
     
   submit = SubmitField("Insert Director")

#######################################################
# Class for inserting a movie
class Movie_Form(FlaskForm):

   title = StringField("Title", 
   validators=[InputRequired(message="You must enter a title"), Length(min=2, max=60, message="Title length must be between 2 and 60 characters")], 
   default="Untitled")
     
   content = StringField("Content", 
   validators=[InputRequired(message="You must the content of a movie"), Length(min=2, max=60, message="File name length must be between 2 and 60 characters")])

   #painter_id = SelectField("Painter ID ", choices=[("1","Manet, Edouard"), ("2","Seurat, Georges")])
   director_id = SelectField("Director ID ")
   #painter_id = QuerySelectField("Painter ID ", query_factory=)    
   
   submit = SubmitField("Insert Movie")

class Delete_Movie_Form(FlaskForm):

   #painter_id = SelectField("Painter ID ", choices=[("1","Manet, Edouard"), ("2","Seurat, Georges")])
   movie_id = SelectField("Movie ", choices=movie_choices)
   #painter_id = QuerySelectField("Painter ID ")    
   
   submit = SubmitField("Delete Movie")