import requests
from bs4 import BeautifulSoup


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



	for tr in soup.findAll("tbody"):
		for td in tr.findAll("td"):
			foodName = td.find('div',class_ = "views-field-field-meal-images-fid")
			attributes = td.find('div',class_ = "views-field-tid")

			zz = attributes.find("div")
			print('hello')
			print(type(zz))

			if(type(attributes)=="bs4.element.Tag"):
				print('good')
				print(zz)
			else:
				print('Nope')
				print(zz)



			if(type(attributes)=="bs4.element.Tag"):
				for attrib in attributes.findAll("div"):




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