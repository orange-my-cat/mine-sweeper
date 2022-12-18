from psycopg2 import connect
import sqlalchemy as db
import os
from werkzeug.security import check_password_hash,generate_password_hash
import unittest
import sys
sys.path.append(os.path.dirname(os.path.abspath("app")))

from app import *
from app.models import *
class UserModelCase(unittest.TestCase):

  def setUp(self):
    basedir = os.path.abspath(os.path.dirname(__file__))
    print(basedir)
    app.config['SQLALCHEMY_DATABASE_URI']=\
        'sqlite:///'+os.path.join(basedir,'test.db')
    self.app = app.test_client()#creates a virtual test environment
    db.create_all()
    u1 = User(username="Test",email="test@test.com",password=generate_password_hash("test1234",method="sha256"),role="user")
    u2 = User(username="Unit",email="unit@test.com",password=generate_password_hash("unit1234",method="sha256"),role="user")
    
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    
  def test_password(self):
    u = User.query.filter_by(username="Unit").first()
    self.assertFalse(check_password_hash(u.password,"testtest"))


  def test_score(self):
    u = User.query.filter_by(username="Unit").first()
    u2 = Score.query.filter_by(user_id=u.user_id).all()
    self.assertFalse(u2)
    s = Score(user_id=u.user_id,score=5)
    db.session.add(s)
    db.session.commit()
    s = Score.query.filter_by(user_id=u.user_id).first()
    assert(s.score!=3)
        
    
  def test_is_committed(self):
    u = User.query.filter_by(username="Test").first()
    self.assertTrue(u)
    
  def test_word_n_choosenword(self):
    w = Wordlist(word="admin")
    w2 = Wordlist(word="table")
    db.session.add(w)
    db.session.add(w2)
    db.session.commit()
    cw = Choosenword(word_id=2,seed=1234)
    db.session.add(cw)
    db.session.commit()
    c1 = Choosenword.query.filter_by(word_id=3).first()
    assert(c1==None)
    c2 = Choosenword.query.filter_by(word_id=2).first()
    assert(c2.seed==1234)          


if __name__=='__main__':
  unittest.main(verbosity=2)

