from flask import Flask

#Flask 'app' variable that we use to access info about the server
app = Flask(__name__)

app.config["Debug"] = True #this is only for testing(remove in final ver.)

#Decorators modify properties of the immediately following function
@app.route("/")

def hello():
	return "Hello World!!!"

#--------

#Routes are paths that the user can visit
#the decorator: app.route("/somepath") ties the decorated function to the path in parenthis

#This is a static route because it returns the same string everytime
@app.route("/name")
def name():
	return "Sam"

#Dynamic route
@app.route("/search/<search_query>")
def search(search_query):
	return search_query

#Adding route
@app.route("/add/<x>/<y>")
def add(x,y):
	return str(int(x)+int(y))


@app.errorhandler(404)
def page_not_found(error):
	return "sorry, this page was not found", 404


#Server will start accepting requests from the client
if __name__ == "__main__":
	#Hosted locally
	app.run(host = "0.0.0.0")































