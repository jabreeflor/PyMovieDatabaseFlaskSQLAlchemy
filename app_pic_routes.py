'''
   import the definitions from app_art_define 
   so that when the user supplies the data we 
   can instantiate a Painter and insert the data 
   into the table
'''
import app_pic_define as my_db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=my_db.engine)
session = Session()

query = session.query(my_db.Movie)
results = query.all()
#for item in results:
#   print ("id={} name={} period={} distance={}".format(item.id, item.name, item.period, item.distance )) 
print(results)
result_dict = [u.__dict__ for u in results]
print(result_dict)

# WTF?
# using flask wt-forms
# run command 
# pip install flask-wtf

from forms_pic import Director_Form, Movie_Form
# note addition of request and redirect to list below
from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

# YOU NEED A SECRET_KEY
# A secret key that will be used for securely signing the 
# session cookie and be used for any other security 
# related needs by extensions or your application. It 
# should be a long random string of bytes, although 
# unicode is accepted too.
app.config["SECRET_KEY"]='why_a_duck?'

####################################################################
# redirect the default route to the form for inserting a new artist 
@app.route("/")
def myredirect():
   return redirect(url_for('director_form'))

###################################################################
# route for inserting an artist
@app.route('/director_form', methods=['GET', 'POST'])
def director_form():
   form = Director_Form()

   #if form.is_submitted():
   #print(form.validate_on_submit())
   if form.validate_on_submit():
      result = request.form
      a_Director = my_db.Director(lastName= result["lastName"], firstName=result["firstName"], country = result["country"], birthDate=result["birthDate"], deathDate=result["deathDate"])
      session.add(a_Director)
      session.commit()  

      return render_template('Director_form_handler.html', title="Insert Director Form Handler", header="Insert Director Form handler", result=result)
   return render_template('Director_form.html', title="Insert Director Form", header="Insert Director Form", form=form)

##########################################################

director_list = session.query(my_db.Director).all()
director_choices = []
for item in director_list:
   mylist=[]
   mylist.append(str(item.id))
   mylist.append("{}, {}".format(item.lastName, item.firstName) )
   my_tuple = tuple(mylist)
   director_choices.append(my_tuple)
print(director_choices)
session.commit()

##########################################################
@app.route('/movie_form', methods=['GET', 'POST'])
def movie_form():
   #form = Painting_Form(from_other=artist_choices)
   form = Movie_Form()
   form.director_id.choices=director_choices
   #form.painter_id.choices=[(1, "Fred"), (2, "Wilma") ]
   print(form.validate_on_submit())
   # KEPT COMING BACK AS INVALID
   if form.validate_on_submit():
   #if form.is_submitted():
      result = request.form
      
      a_movie = my_db.Movie(title= result["title"], content=result["content"] )
      a_movie.director_id = result["director_id"]
      session.add(a_movie)
      session.commit() 
   
      return render_template('movie_form_handler.html', title="Insert Movie Form Handler", header="Insert Movie Form handler", result=result)

   return render_template('movie_form.html', title="Insert Movie Form", header="Insert Movie Form", form=form)

@app.route('/movie_table')
def planet_table():
   return render_template('movie_table.html', title="Movie Table", header="Movie Table", movies=result_dict)



@app.route('/movie_datatable')
def movie_datatable():
   return render_template('movie_datatable.html', title="Movie DataTable", header="Movie DataTable", movies=result_dict)

from forms_pic import Delete_Movie_Form
@app.route('/movie_delete', methods=['GET', 'POST'])
def moviem_delete():
   form = Delete_Movie_Form()

   '''
   added check_same_thread=False in  app_planet_define.py 
   engine = create_engine('sqlite:///planet.db?check_same_thread=False')
   otherwise was getting thread issues
   '''

   # KEPT COMING BACK AS INVALID
   if form.validate_on_submit():
   #if form.is_submitted():
      result = request.form
      
      movie_to_delete = session.query(my_db.Movie).get(int(result["movie_id"]))
      print("Going to delete")
      print(movie_to_delete.title)
      session.delete(movie_to_delete)
      session.commit() 
      
   
      query = session.query(my_db.Movie)
      results = query.all()
      result_dict = [u.__dict__ for u in results]
      

      return render_template('Movie_datatable.html', title="After Deletion", header="After Deletion", movies=result_dict)

   return render_template('Movie_delete.html', title="Delete Movie Form", header="Delete Movie Form", form=form)


if __name__ == "__main__":
   app.run(debug=True)