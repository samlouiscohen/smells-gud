from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import sqlite3 as lite
from sortedFood_crawler import get_foodNames
from contextlib import closing
from flask_mail import Mail, Message


app = Flask(__name__)
app.config.update(
DEBUG = True,
MAIL_SERVER = 'smtp.gmail.com',
MAIL_PORT=465,
MAIL_USE_SSL=True,
MAIL_USERNAME = 'leostilwell@gmail.com',
MAIL_PASSWORD = 'XXXX'
)
mail = Mail(app)
app.config.from_object(__name__)
app.database = "WhatsCookin\'.db"
 


def connect_db():
	return lite.connect(app.database)

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()



@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()



@app.route('/')
def home():
	#init_db()
	g.db = connect_db()
	cur = g.db.execute('select * from entries')
	entries = [dict(food=row[1], attributes = row[2]) for row in cur.fetchall()]
	
	return render_template('index.html', entries = entries)


    #cur = g.db.execute('select food, attributes from entries order by id desc')
    #entries = [dict(food=row[0], attributes=row[1]) for row in cur.fetchall()]
    #return render_template('show_entries.html', entries=entries)

	#return (render_template('show_entries.html', entries=entries))
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


@app.route('/newuser', methods = ['GET','POST'])
def add_User():
	error = None
	g.db = connect_db()
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		preferences = request.form['preferences']
		if(g.db.execute("SELECT EXISTS(SELECT 1 from users WHERE username=username)")):
			print("hi")
			error = 'Invalid username'
			return render_template('index.html')
		else:
			g.db.execute("INSERT INTO users(username,password,email,KeyWords) VALUES(username, password, email, preferences")
			#flash("You are now registered!")
			print("hi")
			return render_template('index.html')
	
	
	g.db.commit()
	g.db.close()
	return render_template('user.html')

app.run()
