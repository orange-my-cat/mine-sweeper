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
# ** Delete
def delete():
    if connection.execute("SELECT count() FROM choosenword where date=date('now','localtime')").all()[0][0]!=0:
        connection.execute(f"DELETE FROM choosenword WHERE date=date('now','localtime');")
        print("Word deleted.")
    else:
        print("There aren't any word for today. Run choose_word.py")
if __name__ == '__main__':
    delete()
