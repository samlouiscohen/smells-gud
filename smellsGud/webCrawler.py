import requests
from bs4 import BeautifulSoup

def getHallInfo(url):

	#Get website page through requests
	source_code = requests.get(url)
	#Convert info into text
	plain_text  =source_code.text
	#Create a BS object to operate on
	soup = BeautifulSoup(plain_text,'lxml')

	#List to hold all foods of one dining hall
	hallFoods =[]

	#Go into 'tbody' and get each 'row'(this is just digging into the html)
	for tr in soup.findAll("tbody"):
		for td in tr.findAll("td"):

			#Hop into HTML containing food names
			foodGenInfo = td.find('a',class_ = "imagefield-field_meal_images")
			
			#Break out current iteration if over total foods in the row
			if(foodGenInfo is None):
				break

			#Get actaul name of food as a string
			foodName = foodGenInfo.get('title')

			#-----Get attributes of each food----

			#Go into '3rd' div down-containing attributes(bs4 Tag)
			attGenInfo = td.find('div',class_ = "views-field-tid")

			#Get all divs(attributes) for particular food
			attGenSpec = attGenInfo.find_all('div')
		
			#List comprehension to store all atttributes in list
			attributes = [prop.text for prop in attGenSpec]
			stringOfAttributes=''
			if len(attributes)==0:
				attributes = "None"
			else:
				for attribute in range(len(attributes)):
					stringOfAttributes+=str(attributes[attribute]) +' '

				attributes = stringOfAttributes[:-1]

					

			#[ [food,[att1,att2,att3]],[food2,[att1,att2,att3]] ]

			#Create list for each food and its attributes
			fullFood = [foodName,attributes]

			#Append each food to a specific halls list
			hallFoods.append(fullFood)

	return hallFoods


def getAllFoods():
	'''Main is calling getTotalInfo for each dininghall'''

	allHallsComplete = []

	for aHall in range(3):
		url = 'http://dining.columbia.edu/?quicktabs_homepage_menus_quicktabs='+str(aHall)+'#quicktabs-homepage_menus_quicktabs'
		
		#Call function for all of a dininghalls food
		aHallFoods = getHallInfo(url)

		#Encompassing list with all dining halls and all their foods
		allHallsComplete.append(aHallFoods)


		print(allHallsComplete)
	return allHallsComplete





