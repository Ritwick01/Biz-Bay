from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

app = Flask(__name__)
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",passwd="password", database="testing")
mycursor = mydb.cursor()
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    mycursor.execute("SELECT * FROM Ads")
    myresult = mycursor.fetchall()
    return render_template('market.html', myresult=myresult)

class RegisterForm(FlaskForm):
    username = StringField(label='Name:')
    age = StringField(label='Age:')
    email_address = StringField(label='Email Address:')
    password1 = PasswordField(label='Password:')
    password2 = PasswordField(label='Confirm Password:')
    phoneno = StringField(label='Phone Number:')
    submit = SubmitField(label='Create Account')

@app.route('/register')
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)