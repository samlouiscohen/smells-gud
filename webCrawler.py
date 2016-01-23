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
	hallFoods = dict()


	#Go into 'tbody' and get each 'row'
	for tr in soup.findAll("tbody"):
		for td in tr.findAll("td"):

			#Get food names
			foodGenInfo = td.find('a',class_ = "imagefield-field_meal_images")#"views-field-field-meal-images-fid"
			
			#Return from the current function if over total foods on page
			if(foodGenInfo is None):
				return
			#print(foodGenInfo)
			foodName = foodGenInfo.get('title')
			print(foodName)


			#Get food attributes
			# attributes = td.find('div',class_ = "views-field-tid")
			# if(attributes is not None):

			# 	print(attributes)


			# if(foodGen is not None):
			# 	print(type(foodGen))

			# 	food2= foodGen.get('title')
			# 	print(food2)
			# else:
			# 	print('fuck u meaty')

				#x = foodGen.find('title')
				#print(x)

				# food2 = foodGen.get('title')

				# print(food2)


			#print(foodGen is None)
			# if not(type(foodGen) == 'NoneType'):
			# 	food2 = foodGen.find('a')
			# 	food3 = food2.find('img',class_ = "title")
			# 	print(food3)
			
			# attributes = td.find('div',class_ = "views-field-tid")
			# print(type(foodName))
			# #print(foodName.toString)
			# x = foodName.get('title')
			# print(x)
			
			# if not(foodName == 'None'):
			# 	r = foodName.find('title')
			# if( not(type(foodName)=='NoneType')):

			# 	fudName = foodName.get("title")

			#zz = attributes.findAll("div")
			#print(foodName)
			# print(fudName)
			#print(zz)
			#print("\n -----")

			# #Control flow, to see if none type or not- so no errors
			# if(type(attributes)=="<class 'bs4.element.Tag'>"):
			# 	print('good')
			# 	print(attributes.find("div"))


			# else:
			# 	print('Nope')
			# 	print(type(attributes))
			# 	#print(attributes.find("div"))



			# if(type(attributes)=="bs4.element.Tag"):
			# 	for attrib in attributes.findAll("div"):
			# 		print('attrib is: ')
			# 		print(attrib)
			# else:
			# 	print('Nope')



			# if(attributes.find(div))
			# for x in attributes.findAll('a'):
				
			# 	#print(foodName)
			# 	print(x)

			
			#print("foodName: " + foodName)
			#print("attributes: " + attributes)



def main():
	'''Main is calling getTotalInfo for each dininghall'''

	diningHallFull = dict()

	for aHall in range(3):
		url = 'http://dining.columbia.edu/?quicktabs_homepage_menus_quicktabs='+str(aHall)+'#quicktabs-homepage_menus_quicktabs'


		diningHallFull['hall'+str(aHall)] = getTotalInfo(url)
	print(diningHallFull)

main()