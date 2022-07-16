from psycopg2 import connect
import sqlalchemy as db
import os
import pandas as pd
import random
import datetime
import sys
basedir = os.path.abspath(os.path.dirname("app"))+"\\app"
engine = db.create_engine('sqlite:///' + os.path.join(basedir, 'database.db'))
connection = engine.connect()

# ** Choosing a word
def choose():
    if connection.execute("SELECT count() FROM choosenword where date=date('now','localtime')").all()[0][0]==0:
        available_word = connection.execute("SELECT COUNT(*) FROM wordlist;").all()[0][0]
        past = connection.execute("SELECT * FROM choosenword ORDER BY date_id DESC LIMIT 5;").all()
        past_seeds = [i[3] for i in past]
        past_words = [i[2] for i in past]
        last_id = past[0][0]
        bool_seed = True
        
        #! Generating seed and word (If the word or seed have been choosen in the past 5 days, the while loop will run until\
        #! a different seed and world is choosen)
        while bool_seed:
            seed_puzzle = random.randint(1,100000)
            no_word = random.randint(1,available_word)
            if seed_puzzle not in past_seeds and no_word not in past_words:
                bool_seed = False
        connection.execute(f"INSERT INTO choosenword VALUES ({last_id+1},date('now','localtime'),{no_word},{seed_puzzle});")
        print("Word for today had been choosen")
    else:
        print("The word for today had been choosen. To delete run delete_word.py")
        
        

if __name__ == '__main__':
    choose()

