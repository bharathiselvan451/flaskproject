from flask import Flask,render_template,flash,request,redirect,url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from datetime import date
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from flask_login import UserMixin

from datetime import timedelta
import os

import smtplib

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisthekey'
db = SQLAlchemy(app)

Gmail = ""



class User(db.Model, UserMixin):
#class User(Base):
    email = db.Column(db.String(20), primary_key=True)
    name = Column(String(20), nullable=False, )
    password = Column(db.String(80), nullable=False)
    budget = Column(db.Integer)
    date = Column(db.String(10))
    expense = Column(db.Integer)
#Base.metadata.create_all(engine)    

   

@app.route('/')
def index():
    return render_template("index.html")
   
@app.route('/login',methods=["GET","POST"])
def index1():
     error = None
     if request.method=="POST":
         email = request.form['log-email']
         global Gmail
         Gmail = email
         password = request.form['log-password']
        
         user = User.query.filter_by(email=email).first()
         
            
         if user:
            if (user.password == password):
                
               return render_template('dashboard.html',expense = user.expense,budget = user.budget)
            else:
                error = "invalid password"
                return render_template('index.html',error=error) 
         else:
            error = "account doesn't exist"
            return render_template('index.html',error=error)         
         
     return render_template('index.html')


@app.route('/register',methods=["GET","POST"])
def index2():
     

    if request.method=="POST":
     try:
         name = request.form['reg-name']
         email = request.form['reg-email']
         global Gmail 
         Gmail= email
         password = request.form['reg-password']
         new_user = User(name=name,email=email,password=password)
         db.session.add(new_user)
         db.session.commit()
         return render_template('dashboard.html')
     except:
        error="EMAIL ID ALREADY EXISTS"
        return render_template('index.html',error=error)
    return render_template('index.html') 
         
@app.route('/budget',methods=["GET","POST"])
def index3():

        if request.method=="POST":
            budget = request.form['budget']
            
            
            user = User.query.filter_by(email=Gmail).first()
            
            today  = date.today()
            if(user.date==None):
                user.date = date.today()
                db.session.add(user)
                db.session.commit()
            
            Begindate = datetime.strptime(user.date, "%Y-%m-%d") 
            Date = Begindate.date()
            if(Date<=today):
               user.budget = budget
               user.date = date.today() + timedelta(days=30)
               db.session.add(user)
               db.session.commit()
               return render_template("budgetsetter.html")
            else:

               error="NOT 30 DAYS YET"
               return render_template('budgetsetter.html',error=error)
            
        return render_template("budgetsetter.html")    

@app.route('/setexpense',methods=["GET","POST"])
def index4():
          if request.method=="POST":
            expense =int( request.form['TExpenses'])
            user = User.query.filter_by(email=Gmail).first()
            if(user.expense==None):
                user.expense = 0
            currentexpense = user.expense+expense
            if(currentexpense>user.budget):
                error="mail sent"
                server = smtplib.SMTP('smtp.gmail.com',587)
                server.starttls()
                server.login('YOUR_MAIL','')
                server.sendmail('YOUR_MAIL',Gmail,'MONTHLY BUDGET EXCEEDED - peta team')
                return render_template('dashboard.html',error=error,expense = user.expense,budget = user.budget)
            else:
                user.expense = currentexpense
                db.session.add(user)
                db.session.commit()
                return render_template('dashboard.html',expense = user.expense,budget = user.budget)   
          return render_template('dashboard.html',expense = user.expense,budget = user.budget)     

if __name__ == '__main__':
    app.run(host='0.0.0.0')

         


        
