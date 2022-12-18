from wsgiref.util import request_uri
from flask import render_template,redirect,url_for,flash,request,make_response,session,jsonify
from flask_login import login_user,login_required,logout_user,current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_admin.menu import MenuLink
from werkzeug.security import check_password_hash,generate_password_hash
from werkzeug.urls import url_parse
from app.models import *
from app import app, db
from app.forms import SignUpForm,LoginForm
import datetime
import json
import pandas as pd
import numpy as np
from scipy import stats


#Admin View Classes -->
class AdminModelView(ModelView):
    def is_accessible(self):
      return current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs): #redirect for non-admin role
        if not self.is_accessible():
            return redirect(url_for('login',next=request.url)) 

class AdminUserView(AdminModelView):
   column_searchable_list = ['username', 'email','role']

class AdminScoreView(AdminModelView):
   column_searchable_list = ['date','user_id','score']
         
class AdminWordView(ModelView):
   column_searchable_list = ['word']
   
class HomeAdminView(AdminIndexView):
    def is_accessible(self):
      return current_user.role == "admin"
    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login',next=request.url))     
   
#* Admin Page Configuration
admin = Admin(app,index_view=HomeAdminView(),template_mode="bootstrap4")
admin.add_view(AdminUserView(User, db.session))
admin.add_view(AdminScoreView(Score, db.session))
admin.add_view(AdminWordView(Wordlist, db.session))
admin.add_view(AdminModelView(Choosenword, db.session))
admin.add_link(MenuLink(name='Logout',url='/logout',class_name="btn btn-outline-warning me-2"))


@app.before_request
def make_session_permanent():
    session.permanent = True
    session.modified = True

#** The home page of the application.
@app.route('/')
def index():
   today = Choosenword.query.filter_by(date=datetime.date.today()).first()
   word = Wordlist.query.filter_by(word_id=today.word_id).first().word
   seed = today.seed
   #!! If user is sign in, it will render user.html
   #!! If user is admin, it will redirect to /admin
   #!! else it will render index.html
   if current_user.is_authenticated == 0:  
         return render_template("index.html",word=word,seed=seed)
   else:
      if  current_user.role == "admin":
         return redirect("/admin")
      else:
         #? If a user had managed to get the correct answer for that day. Then user is not allowed to attempt the puzzle again for that day
         score = Score.query.filter_by(user_id=current_user.user_id,date=datetime.date.today()).first()
         if score:
            return render_template('user.html',name=current_user.username,attempted=1,word=word,seed=seed,user_id=current_user.user_id)
         else:
            return render_template('user.html',name=current_user.username,attempted=0,word=word,seed=seed,user_id=current_user.user_id)
   
#** The login page
@app.route("/login",methods=['GET','POST'])
def login():
   
   if current_user.is_authenticated:
      return redirect('/')
   form = LoginForm()
   if form.validate_on_submit():
      user = User.query.filter_by(username=form.username.data).first()
      
      if user is None or not check_password_hash(user.password,form.password.data): #if the user doesn't exist or if check password is false
         flash("Invalid username or password")
         return redirect("/login")
      
      login_user(user,remember=form.remember_me.data) 
      if user.role=="admin": #take to admin page
         return redirect('/admin')
      response = make_response(redirect('/'))
      response.set_cookie('user', user.username, expires=datetime.datetime.now()+datetime.timedelta(days=30))
      return response   

   return render_template("login.html",form=form)

#** The sign up page
@app.route("/signup",methods=['GET','POST'])
def signup():
   form = SignUpForm()
   if form.validate_on_submit():
      new_user = User(username=form.username.data,email=form.email.data,password=generate_password_hash(form.password.data,method="sha256"),role="user")
      db.session.add(new_user)
      db.session.commit()
      flash('Congratulations, you are now a registered user!')
      return redirect("/login")
   return render_template("signup.html",form=form)

#** When a login user submit a guess and the guess is correct, a XMLHTTPREQUEST "POST" will send the number of guesses and the following will run.
@app.route('/submit/<string:counter>',methods=['POST'])
def submit(counter):
   if current_user.is_authenticated ==1:
      counter = json.loads(counter)
      new_entry = Score(user_id=current_user.user_id,score=int(counter))
      db.session.add(new_entry)
      db.session.commit()
   return redirect('/')
   
      
#** Allow signed in user to obtain data for the statistics modal
@app.route('/result',methods=["GET"])
def result():
   if current_user.is_authenticated == 1:
      # ** The score of the user
      score_all = Score.query.filter(Score.user_id==current_user.user_id ,Score.date>=datetime.date.today()-datetime.timedelta(days=7)).all()
      print(score_all)
      # ** Check whether a user had any attempts in the past 7 days
      if len(score_all)!=0:
         score=[i.score for i in score_all]
         date = [i.date.strftime('%Y-%m-%d') for i in score_all]
         jsonData = []
         for i in range(len(score)):
            jsonData.append({"x":date[i],"y":score[i]})
         
         # ** Median score of other people
         score_other = Score.query.filter(Score.date>=datetime.date.today()-datetime.timedelta(days=7)).all()
         score2=[i.score for i in score_other]
         date2 = [i.date.strftime('%Y-%m-%d') for i in score_other]
         df=pd.DataFrame(list(zip(date2,score2)),columns=["x","y"])
         sub_df1=df_to_json(df,0.9)
         sub_df2=df_to_json(df,0.5)
         sub_df3=df_to_json(df,0.1)
         
         #** the score out of 100 when compared to other user
         sub_df4=rank_score(df,score,date)
         jsonData2 = []
         for i in range(len(sub_df4[0])):
            jsonData2.append({"x":date[i],"y":sub_df4[0][i]})
         return jsonify(jsonData,sub_df1,sub_df2,sub_df3,round(sum(score)/len(score),3),round(sub_df4[1],3),len(score),jsonData2)
      else:
         # ** Median of other people
         score_other = Score.query.filter(Score.date>=datetime.date.today()-datetime.timedelta(days=7)).all()
         score2=[i.score for i in score_other]
         date2 = [i.date.strftime('%Y-%m-%d') for i in score_other]
         df=pd.DataFrame(list(zip(date2,score2)),columns=["x","y"])
         
         sub_df1=df_to_json(df,0.9)
         sub_df2=df_to_json(df,0.5)
         sub_df3=df_to_json(df,0.1)
         return jsonify(None,sub_df1,sub_df2,sub_df3,None,None,0,None)
   return redirect("/")

#** The function used to get the different percentile
def df_to_json(df,percentile):
   sub = df.groupby("x").quantile(percentile)
   sub.index.name = "x"
   sub.reset_index(inplace=True)
   jsonData = []
   for i in range(sub.shape[0]):
      jsonData.append({"x":sub.iloc[i,0],"y":sub.iloc[i,1]})
   return jsonData

#** The function used to get score out of 100 for a user.
def rank_score(df,score,date):
   score_list=[]
   for i,date in enumerate(date):
      df_date=list(df.loc[df['x']==date,'y'])
      if len(df_date)==1:
         score_list.append(100)
      else:
         score_list.append(100-stats.percentileofscore(df_date,score[i]))
   return score_list,sum(score_list)/len(score_list)
   
   
#** The admin page
@app.route("/admin")
def admin():
   if current_user.is_authenticated ==0:
      return redirect('login')
   if  current_user.role != "admin":
      return redirect('/')
   return redirect('/admin')

#** The logout mechanism
@app.route('/logout')
@login_required
def logout():
   logout_user()
   response = make_response(redirect('/'))
   response.delete_cookie('user')
   return response 

@app.route('/shareresult',methods=["GET"])
def shareresult():
   userParam = request.args.get('user', default = "", type = str)
   if userParam != "":
      score_all = Score.query.filter(Score.user_id==userParam ,Score.date>=datetime.date.today()-datetime.timedelta(days=7)).all()
      score=[i.score for i in score_all]
      date = [i.date.strftime('%Y-%m-%d') for i in score_all]
      jsonData = []
      for i in range(len(score)):
         jsonData.append({"x":date[i],"y":score[i]})
           
      # ** Median of other people
      score_other = Score.query.filter(Score.date>=datetime.date.today()-datetime.timedelta(days=7)).all()
      score2=[i.score for i in score_other]
      date2 = [i.date.strftime('%Y-%m-%d') for i in score_other]
      df=pd.DataFrame(list(zip(date2,score2)),columns=["x","y"])
      
      sub_df1=df_to_json(df,0.9)
      sub_df2=df_to_json(df,0.5)
      sub_df3=df_to_json(df,0.1)
      
      return jsonify(jsonData,sub_df1,sub_df2,sub_df3,)
   return redirect('/')

@app.route('/share',methods=["GET"])
def share():
   return render_template("share.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
 
#error handling 500 
@app.errorhandler(500)
def other_error(e):
    return render_template('500.html'), 500