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

# ** Adding a word into the database
def add(word):
    if connection.execute(f"SELECT count() FROM wordlist where word='{word}'").all()[0][0]==0:
        connection.execute(f"INSERT INTO wordlist (word) VALUES ('{word}');")
        print("Success")
    else:
        print("The word is in the database.")
        

if __name__ == '__main__':
    for word in sys.argv[1:]:
        #** Check if a word has 5 characters
        if len(word)==5 and "x" not in word:
            add(word)
        else:
            print("Error")
