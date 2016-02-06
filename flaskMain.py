from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3 as lite
from webCrawler import getAllFoods
from contextlib import closing
from flask_mail import Mail, Message


app = Flask(__name__)

app.config.from_object(__name__)
app.config.update(
DEBUG = True,
MAIL_SERVER = 'smtp.gmail.com',
MAIL_PORT=465,
MAIL_USE_SSL=True,
MAIL_USERNAME = 'smellzgud@gmail.com',
MAIL_PASSWORD = 'Columbia'
)

#Create mail object
mail = Mail(app)
app.config.from_object(__name__)

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

#-------End of database-----



sched = BackgroundScheduler()

#task called by heroku scheduler add-on
@sched.scheduled_job('interval',seconds=10)
def send_Mail():
	with app.app_context():
	# with mail.connect() as conn:
 #    	for user in users:
 #        	message = '...'
 #        	subject = "hello, %s" % user.name
 #        	msg = Message(recipients=[user.email],
 #            	body=message,
 #                subject=subject)

 #        	conn.send(msg)

		msg = Message("Mail Test",
			sender = 'smellzgud@gmail.com',
			recipients = ['ls3223@columbia.edu'])
	
		g.db = connect_db()
		cur = g.db.execute('select * from entries order by id desc')
		data = cur.fetchall()
		for row in data:
			entries = dict(food=row[1],attributes=row[2])
		cur.close()
		toSend =', '.join("{!s}={!r}".format(key,val) for (key,val) in entries.items())
		
		cur1 = g.db.execute('select email from users')
		data1 = cur1.fetchall()
		
		for row in data1:
			print(row[0])
			message = Message(sender = 'smellzgud@gmail.com',
				recipients=[row[0]],body=toSend)
			message.body = toSend
			mail.send(message)
		
sched.add_job(send_Mail,"interval",minutes=1)
sched.start()




#Route for the website(landing page of website)
@app.route('/')
def home():
	
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

	g.db.close()

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

@app.route('/mail')
def send_Mail():
	msg = Message("Mail Test",
		sender = 'smellzgud@gmail.com',
		recipients = ['ls3223@columbia.edu'])
	
	g.db = connect_db()
	cur = g.db.execute('select * from entries order by id desc')
	data = cur.fetchall()
	for row in data:
		entries = dict(food=row[1],attributes=row[2])

	toSend =', '.join("{!s}={!r}".format(key,val) for (key,val) in entries.items())

	msg.body = toSend
	mail.send(msg)
	return render_template('mail.html')

@app.route('/add_grouping',methods = ['GET','POST'])
def add_grouping():
	pass


app.run(host='0.0.0.0')

