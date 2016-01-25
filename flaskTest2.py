from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import sqlite3 as lite
from webCrawler import getAllFoods
from contextlib import closing
from flask_mail import Mail, Message
import os


app = Flask(__name__)
app.config.update(
DEBUG = True,
MAIL_SERVER = 'smtp.gmail.com',
MAIL_PORT=465,
MAIL_USE_SSL=True,
MAIL_USERNAME = 'leostilwell@gmail.com',
MAIL_PASSWORD = 'XXXX'
)
port = int(os.environ.get("PORT",5000))

#Create mail object
mail = Mail(app)
app.config.from_object(__name__)

app.config["DEBUG"] = True
app.database = "WhatsCookin\'.db"


food = []
food = getAllFoods()
FullLength = len(food)
length1 = len(food)



#Create variable to reference database file
app.database = "WhatsCookin\'.db"
 
#Creates a connection

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


#Route for the website(landing page of website)
@app.route('/')
def home():
	#food = []
	food = getAllFoods()
	FullLength = len(food)
	length1 = len(food)
	g.db = connect_db()
	
	#g.db.execute("INSERT INTO entries(food,attributes) VALUES('chicken')")
	for x in range(FullLength):
		
		for y in range(len(food[x])):
			if len(food[x][y][1]) == "none" :
				g.db.execute("INSERT INTO entries(food,attributes) VALUES(?,?)",[food[x][y][0],food[x][y][1]])
				g.db.commit()
			else:
				g.db.execute("INSERT INTO entries(food,attributes) VALUES(?,?)",[food[x][y][0],food[x][y][1]])
				g.db.commit()




	g.db = connect_db()
	#Get everything from entries

	cur = g.db.execute('select * from entries')
	#Create dictionary using list comprehension
	entries = [dict(food=row[1], attributes = row[2]) for row in cur.fetchall()]
	
	#Returns the html to user
	return render_template('index.html', entries = entries)


	
    

#------Mail aspect of website-----



@app.route('/mail')
def send_Mail():
	#toSend = ""
	msg = Message("Mail Test",
		sender = 'leostilwell@gmail.com',
		recipients = ['slc2206@columbia.edu'])
	
	g.db = connect_db()
	cur = g.db.execute('select * from entries order by id desc')
	data = cur.fetchall()
	for row in data:
		entries = dict(food=row[1],attributes=row[2])

	toSend =', '.join("{!s}={!r}".format(key,val) for (key,val) in entries.items())

	print (toSend)

	
	msg.body = toSend
	mail.send(msg)
	return render_template('mail.html')






#Connecting two pages
@app.route('/goToRegister')
def goNextPage():
	return redirect("")





#Route to add user preferences
@app.route('/add_grouping', methods = ['GET','POST'])
def add_group():
	pass

























#Route to add users 

@app.route('/adduser', methods = ['GET','POST'])
def add_User():
	error = None
	g.db = connect_db()
	cur = g.db.cursor()
	if request.method == "POST":
		#set variables from web form
		username = request.form["username"]
		password = request.form["password"]
		email = request.form["email"]
		preferences = request.form["preferences"]
		
		#if the username entered is already in db, redirect to homepage
		if(g.db.execute("SELECT EXISTS(SELECT 1 from users WHERE username==username)")==1):
			#print("hi")
			error = 'Invalid username'
			return redirect('http://127.0.0.1:5000/')
			
		g.db.execute("INSERT INTO users(username,password,email) VALUES(?,?,?)",[request.form['username'], request.form['password'], request.form['email']])
		#flash("You are now registered!")
		#print("hi")
		return redirect('http://127.0.0.1:5000/thankyou')
	
	
	g.db.commit()
	g.db.close()
	return render_template('adduser.html')

@app.route('/thankyou')
def thankyou():
	return render_template('thankyou.html')


app.run()
