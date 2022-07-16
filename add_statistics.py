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

# ** Adding  the statistic table
def add():
    connection.execute("""DELETE FROM score where date >= date('now','-7 day','localtime');""")
    connection.execute("""INSERT INTO score (date,user_id,score) VALUES 
(date("now","-7 day",'localtime'),1,6),
(date("now","-7 day",'localtime'),2,7),
(date("now","-7 day",'localtime'),3,3),
(date("now","-7 day",'localtime'),4,8),
(date("now","-7 day",'localtime'),5,7),
(date("now","-7 day",'localtime'),6,8),
(date("now","-6 day",'localtime'),1,2),
(date("now","-6 day",'localtime'),2,6),
(date("now","-6 day",'localtime'),3,6),
(date("now","-6 day",'localtime'),4,6),
(date("now","-6 day",'localtime'),5,7),
(date("now","-6 day",'localtime'),6,7),
(date("now","-5 day",'localtime'),1,8),
(date("now","-5 day",'localtime'),2,2),
(date("now","-5 day",'localtime'),3,9),
(date("now","-5 day",'localtime'),4,3),
(date("now","-5 day",'localtime'),5,10),
(date("now","-5 day",'localtime'),6,8),
(date("now","-4 day",'localtime'),1,8),
(date("now","-4 day",'localtime'),2,3),
(date("now","-4 day",'localtime'),3,9),
(date("now","-4 day",'localtime'),4,6),
(date("now","-4 day",'localtime'),5,5),
(date("now","-4 day",'localtime'),6,4),
(date("now","-3 day",'localtime'),1,8),
(date("now","-3 day",'localtime'),2,2),
(date("now","-3 day",'localtime'),3,3),
(date("now","-3 day",'localtime'),4,7),
(date("now","-3 day",'localtime'),5,4),
(date("now","-3 day",'localtime'),6,7),
(date("now","-2 day",'localtime'),1,2),
(date("now","-2 day",'localtime'),2,10),
(date("now","-2 day",'localtime'),3,3),
(date("now","-2 day",'localtime'),4,9),
(date("now","-2 day",'localtime'),5,7),
(date("now","-2 day",'localtime'),6,6),
(date("now","-1 day",'localtime'),1,8),
(date("now","-1 day",'localtime'),2,3),
(date("now","-1 day",'localtime'),3,8),
(date("now","-1 day",'localtime'),4,3),
(date("now","-1 day",'localtime'),5,7),
(date("now","-1 day",'localtime'),6,3);""")
    print("Success")
        
        

if __name__ == '__main__':
    add()


