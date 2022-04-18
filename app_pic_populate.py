'''
  This code will populate the tables defined in app_art_define
  Separating the populate code from the define code allows other 
  code to access the definitions without "re-populating" the 
  database tables
'''
import app_pic_define as my_db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=my_db.engine)
session = Session()

#################################################################
# initially populate database tables from a JSON file 
import json
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open('static/data/director_data.json') as f:
   pic = json.load(f)

# to have access to the list element and its index 
# you can use enumerate
for i, director in enumerate(pic["directors"]):
   # print("{} -- {} {}".format(i, artist["firstName"], artist["lastName"]))
   a_director = my_db.Director(lastName=director["lastName"], firstName=director["firstName"], 
   country=director["countryName"], birthDate=director["birthDate"], 
   deathDate=director["deathDate"]) 
   session.add(a_director)
   session.flush()  
   # https://stackoverflow.com/questions/17325006/how-to-create-a-foreignkey-reference-with-sqlalchemy
   # flush the session so that the painter is assigned an id    
   
   for j, movie in enumerate(pic["directors"][i]["movies"]):
      # print("\t", chr(97+j), art["painters"][i]["paintings"][j]["title"])
      a_movie = my_db.Movie(title=movie["title"], content=movie["content"])
      a_movie.director_id = a_director.id
      session.add(a_movie)


session.execute(my_db.taken_table.insert().values([(1, 3), (2, 3)]))
session.commit()

session.execute(my_db.taken_table.insert().values([(2, 4), (3, 2)]))
session.commit()

session.commit()
#Single Table
query = session.query(my_db.Movie)
results = query.all()
for item in results:
   print ("id={} title={} content={} director_id={}".format(item.id, item.title, item.content, item.director_id )) 

print("\n")
#many tables
direct = session.query(my_db.Director).first()
print("{} {} took the following coureses:".format(direct.firstName, direct.lastName))
for dir in direct.movies:
   print(dir.title)