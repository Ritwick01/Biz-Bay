from flask import Flask, render_template
app = Flask(__name__)
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",passwd="password", database="testing")
mycursor = mydb.cursor()

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    mycursor.execute("SELECT * FROM Ads")
    myresult = mycursor.fetchall()
    return render_template('market.html', myresult=myresult)