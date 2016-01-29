from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import sqlite3 as lite
from webCrawler import getAllFoods
from contextlib import closing
from flask_mail import Mail, Message



app = Flask(__name__)

app.config.from_object(__name__)
app.config["DEBUG"] = True
app.database = "WhatsCookin\'.db"


#Create the database
def connect_db():
	return lite.connect(app.database)

#Creates the database if it doesnt exist
def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
	db.commit()


#Allows flask to communcate with the database
@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

#-------End of data base-----






#Route for the website(landing page of website)
@app.route('/')
def home():
	print('why')
	#Returns the html to user
	return render_template('homePage.html')

	#Get foods from webcrawler and store in database
	foods = getAllFoods()
	foodsLen = len(foods)

	#We open a database connection #######**@#$*%*@#this was g.db
	g.database = connect_db()
	
	for x in range(FullLength):
		
		for y in range(len(food[x])):
			if len(food[x][y][1]) == "none" :
				g.db.execute("INSERT INTO entries(food,attributes) VALUES(?,?)",[food[x][y][0],food[x][y][1]])
				g.db.commit()
			else:
				g.db.execute("INSERT INTO entries(food,attributes) VALUES(?,?)",[food[x][y][0],food[x][y][1]])
				g.db.commit()



@app.route('/add_user', methods = ['POST'])
def add_user():
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']

	#We open a database connection when we add a user(and their info)
	g.database = connect_db()
	#Specifiys location for data- into user info column
	g.database.execute("INSERT INTO users(username,password,email) VALUES(?,?,?)",[username,password,email])

	print("The email addreess is:"+email)

	cur = g.database.cursor()

	cur = g.db.execute('select * from entries')
	#Create dictionary using list comprehension
	entries = [dict(food=row[1], attributes = row[2]) for row in cur.fetchall()]





	#Render the next webpage(step of progress)
	return render_template('preferences_page.html',entries = entries)



@app.route('/add_grouping',methods = ['GET','POST'])
def add_grouping():
	pass










if __name__ == "__main__":
	app.run(debug=True, port=33507)

