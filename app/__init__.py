from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import datetime
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
import random


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# ** FLASK environment configuration
app.config['SECRET_KEY'] = "secretkey"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir, 'database.db')

# ** Database Configuration
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# ** Login Configuration
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"

from app import routes,models
# ** Schedule Function (Will run at 12.00 am if deploy at a server)
def choose():
    #! Get the number of word present in the wordlist table
    available_word = db.session.query(models.Wordlist).count()
    #! Get the rows for the past 5 days from choosenword table (Note assuming only one row in this tablefor a particular day)
    past = db.session.query(models.Choosenword).order_by(models.Choosenword.date_id.desc()).limit(5).all()
    past_seeds = [i.seed for i in past]
    past_words = [i.word_id for i in past]
    bool_seed = True
    
    #! Generating seed and word (If the word or seed have been choosen in the past 5 days, the while loop will run until\
    #! a different seed and world is choosen)
    while bool_seed:
        seed_puzzle = random.randint(1,100000)
        no_word = random.randint(1,available_word)
        if seed_puzzle not in past_seeds and no_word not in past_words:
            bool_seed = False
    new_choosenword = models.Choosenword(word_id = no_word,seed=seed_puzzle)
    db.session.add(new_choosenword)
    db.session.commit()

sched = BackgroundScheduler(daemon=True)
sched.add_job(choose,'cron',day="*")
sched.start()
