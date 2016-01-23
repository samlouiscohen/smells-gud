import requests
from bs4 import BeautifulSoup

#/Users/samcohen/GitHub/WhatsCookin
#/Users/samcohen/Desktop/Programming/WebApps/smellsGud

def getTotalInfo(url):

	#Get website page through requests
	source_code = requests.get(url)
	#Convert info into text
	plain_text  =source_code.text
	#Create a BS object to operate on
	soup = BeautifulSoup(plain_text,'lxml')


	#---------------
	numFoods = range(10) 
	completeHalls = dict()
	numColumbiaDiningHalls = range(1)
	#hallFoods = dict()

	hallFoods =[]
	#print("WOOP")
	#Go into 'tbody' and get each 'row'
	for tr in soup.findAll("tbody"):
		for td in tr.findAll("td"):

			#Get food names
			foodGenInfo = td.find('a',class_ = "imagefield-field_meal_images")#"views-field-field-meal-images-fid"
			
			#Return from the current function if over total foods on page
			if(foodGenInfo is None):
				break
			foodName = foodGenInfo.get('title')

			#-----Get attributes of each food----

			#Go into '3rd' div containing attributes(bs4 Tag)
			attGenInfo = td.find('div',class_ = "views-field-tid")

			#Get all divs(attributes) for particular food
			attGenSpec = attGenInfo.find_all('div')
		
			#List comprehension to store all atttributes in list
			attributes = [prop.text for prop in attGenSpec]

			#[ [food,[att1,att2,att3]],[food2,[att1,att2,att3]] ]

			#Create list for each food and its attributes
			fullFood = [foodName,attributes]

			#Append each food to a specific halls list
			hallFoods.append(fullFood)

		print(hallFoods)


	return hallFoods


def main():
	'''Main is calling getTotalInfo for each dininghall'''

	diningHallFull = []

	for aHall in range(3):
		url = 'http://dining.columbia.edu/?quicktabs_homepage_menus_quicktabs='+str(aHall)+'#quicktabs-homepage_menus_quicktabs'
		
		#Call function for all of a dininghalls food
		aHallFoods = getTotalInfo(url)

		#Encompassing list with all dining halls and all their foods
		diningHallFull.append(aHallFoods)

	print(diningHallFull)

main()