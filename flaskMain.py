from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3 as lite
from webCrawler import getAllFoods
from contextlib import closing
from flask_mail import Mail, Message


app = Flask(__name__)

app.config.from_object(__name__)
app.config["DEBUG"] = True
app.database = "WhatsCookin\'.db"

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

#Create the database------------------------------------------------------------
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

#End of data base---------------------------------------------------------------


sched = BackgroundScheduler()
dbSched = BackgroundScheduler()

#repopulates the database with any unseen foods every 24 hours
@dbSched.scheduled_job('interval',hours=24)
def populate_Db():
	with app.app_context():
		allHalls = getAllFoods()
		numDininghalls = len(allHalls)

		#We open a database connection
		g.db = connect_db()
	



		for aHall in range(numDininghalls):

			for aFood in range(len(allHalls[aHall])):

				# g.db.execute("INSERT INTO entries(food,hall) VALUES(?,?)",[allHalls[aHall][aFood][0],aHall])
			
				print("LOKOOKOKOKOK")
				print(allHalls[aHall][aFood][1])

				#Store attributes as one string to later be broken into components
				attString = ''
				for att in allHalls[aHall][aFood][1]:

					attString +=(att+', ')

				#Removed excess comma
				allAttString = attString[:-2]


				print("HEKFSDGSDGSDFGSD")
				print(allAttString)

				g.db.execute("INSERT INTO entries(food,attributes,hall) VALUES(?,?,?)",[allHalls[aHall][aFood][0],allAttString,aHall])

			# g.db.execute("INSERT INTO entries(food) VALUES(?)",[allHalls[aHall][aFood][0]])
				g.db.commit()

			# if not(len(allHalls[aHall][aFood][1]) == 0):
			# 	print("this was not zero!!")
				#for att in range(len(allHalls[aHall][aFood][1])):
				# 	#Dont dont attach 'empty' attributes to a food
				# 	print(allHalls[aHall][aFood][1])
				# # if (len(allHalls[aHall][aFood][1]) == 0):
				# # 	print("This was empty!!")
					#g.db.execute("INSERT INTO entries(attributes) VALUES(?)",[allHalls[aHall][aFood][1][att]])
					#g.db.commit()
			# else:
			# 	g.db.execute("INSERT INTO entries(food,hall) VALUES(?,?)",[allHalls[aHall][aFood][0],aHall])
			# 	g.db.commit()

	print('Close database!')
	g.db.close()
#task called by heroku scheduler add-on
@sched.scheduled_job('interval',hours=24)
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
		
sched.add_job(send_Mail,"interval",hours=24)
sched.start()


#Route for the website(landing page of website)
@app.route('/')
def home():
	#Returns the html to user
	return render_template('homePage.html')




@app.route('/add_user', methods = ['POST'])
def add_user():
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']

	#We open a database connection when we add a user(and their info)
	print('Reconnect to database')
	g.db = connect_db()

	print('insert!!!')
	print('username: '+username)
	print('password: '+password)
	print('email: '+email)
	#Specifiys location for data- into user info column
	g.db.execute("INSERT INTO users(username,password,email) VALUES(?,?,?)",[username,password,email])
	g.db.commit()
	print("The email addreess is:"+email)

	cur = g.db.cursor()

	cur = g.db.execute('select * from entries')

	#Pull foods from data base to show on second page
	entries = [dict(food=row[1], attributes = row[2]) for row in cur.fetchall()]

	g.db.close()



	#Render the next webpage(step of progress)
	return render_template('preferences_page.html',entries = entries)


@app.route('/add_grouping',methods = ['GET','POST'])
def add_grouping():
	pass


@app.route('/get_checkboxes',methods = ['POST'])
def get_checkboxes():
	food = request.form['foodName']
	#group = request.form['group']
	g.db = connect_db()

	g.db.execute("INSERT INTO users(favorites) VALUES(?)",[food])
	# g.db.execute("INSERT INTO users(favorites,groups) VALUES(?,?)",[food,group])


	g.db.close()





#Now you have to run with this command: gunicorn flaskMain:app
#Set the host to be 0.0.0.0
if __name__ == '__main__':
    app.run(debug=True)
