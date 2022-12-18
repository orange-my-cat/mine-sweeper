from enum import unique
from wsgiref import validate
from flask_login import UserMixin
from sqlalchemy.orm import validates
from app import app,db,login_manager
import datetime

# ** The classes for the database table

# ** Keep track of the users' login information
class User(UserMixin,db.Model):
   user_id = db.Column(db.Integer,primary_key=True)
   username = db.Column(db.String(15),index=True,unique=True)
   email = db.Column(db.String(50),index=True,unique=True)
   password = db.Column(db.String(128))
   role = db.Column(db.String(8))
   scores = db.relationship("Score",backref='user',lazy=True)
   def get_id(self):
      return (self.user_id)

# ** Keep track of the score of a user 
# !! Only one attempt per day so the date and user_id should be unique
class Score(db.Model):
   score_id = db.Column(db.Integer,primary_key=True)
   date = db.Column(db.Date, default=datetime.date.today)
   user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)
   score = db.Column(db.Integer)

# ** List of words that can be used for the game
class Wordlist(db.Model):
   word_id = db.Column(db.Integer,primary_key=True)
   word = db.Column(db.String(5),index=True,unique=True)
   choosen_words = db.relationship("Choosenword",backref='choosen_word',lazy=True)
   
   @validates("word") 
   def validate_word(self,key,value):
      if 'x' in value:
         raise ValueError("x should not be included")
      return value

# ** Keep track of what word and seed is choosen
class Choosenword(db.Model):
   date_id = db.Column(db.Integer,primary_key=True)
   date = db.Column(db.Date, default=datetime.datetime.today, unique = True)
   word_id = db.Column(db.Integer,db.ForeignKey('wordlist.word_id'),nullable=False)
   seed = db.Column(db.Integer)

   

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))