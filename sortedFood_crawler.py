import requests
from bs4 import BeautifulSoup
import sqlite3 as lite



def get_foodNames(url):

	food_list = []
	vegetarian_list = []
	meatlovers_list = []
	favoriteFood_list =[] #This will require work

	source_code = requests.get(url)

	plain_text = source_code.text

	soup = BeautifulSoup(plain_text,'lxml')


	for name in soup.findAll("a",{"imagefield-field_meal_images"}):

		food = name.get('title')
		food_list.append(food)
	return food_list



'''Food grouping:

* Refreshmenu(someNumber) is:
	rel = "gallery-someNumber"

vegan is filter_menus(7481,4)
gluten-free 10

'''


def getTotalInfo(url):
	

	

	#for aHall in range(1):



	#url = 'http://dining.columbia.edu/?quicktabs_homepage_menus_quicktabs='+str(aHall)+'#quicktabs-homepage_menus_quicktabs'

	#Specific soup/requests Stuff
	source_code = requests.get(url)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text,'lxml')

	vegetarian_list = []

	#Calculating this is still up in the air, maybe a eventaul large # and a try-executive
	numFoods = range(10) 
	completeHalls = dict()
	numColumbiaDiningHalls = range(1)
	hallFoods = dict()
	for colNum in numFoods:
		aFoodsCatagories = []

		for tableData in soup.findAll("td",{"col-"+str(colNum)}):
			#print('hello')
			#links = tableData.findAll('a')

			#Keep in mind: for i,j in tableData.find(some, some2)

			for food in tableData.findAll(("a",{"imagefield-field_meal_images"})):
				foodName = food.get('title')
				#Eventually 0 will be designated by a variable in the URL
				
				#hallFoods.append(str(food))
				#g = 7
			
		#Add total foods to this iterations hall
		#diningHall_menus['hall'+str(hallNum)] = get_food_names(url)
	

			for catagories in tableData.findAll("span",{"field-content"}):

				for aCatagory in catagories.findAll("div"):
					#print(type(aCatagory))

					catagoryFull = str(aCatagory)
					# <div class="Vegetarian">Vegetarian</div> so use splits
					catagory_firstCut = catagoryFull.split(">")
	
					catagory_secondCut = catagory_firstCut[1].split("<")

					catagory = catagory_secondCut[0]

					aFoodsCatagories.append(str(catagory))

					#print(catagory)
					#print(aCatagory)

			#foodName = links.findAll(("a",{"imagefield-field_meal_images"}))
			#print(links)
			#print(type(links))
			hallFoods[str(foodName)] = aFoodsCatagories

	return hallFoods

	#completeHalls['hall'+str(aHall)] = hallFoods




def main():
	diningHallFull = dict()

	for aHall in range(3):
		url = 'http://dining.columbia.edu/?quicktabs_homepage_menus_quicktabs='+str(aHall)+'#quicktabs-homepage_menus_quicktabs'


		diningHallFull['hall'+str(aHall)] = getTotalInfo(url)
	print(diningHallFull)

	con = lite.connect('WhatsCookin\'.db')
	with con:
		cur = con.cursor()
		#cur.execute("INSERT INTO entries VALUES(1, 'chicken', 'vegetarian')")
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM entries")

		rows = cur.fetchall()
		#for row in rows:
			#print (row)

	con.close()
main()

#PLEASE WORK ONE DAY

"""			for food,catagories in tableData.findAll(("a",{"imagefield-field_meal_images"}),("span",{"field-content"})):
				print("within the loop[][][][][")
				foodName = food.get('title')
				print(foodName)
				for aCatagory in catagories.findAll("div"):
					catagoryFull = str(aCatagory)
					print(catagoryFull)
"""







'''		for name in soup.findAll("a",{"imagefield-field_meal_images"}):
		

		foodName = name.get('title')
		

		print(foodName)





	allFoods = {}






	for colNum in range(5,7):
		print(colNum)
		print(type(soup))
		aColumn = 'col-'+str(colNum+1) #This is at 5 now bc of 0+1

		for name in soup.findAll("a",{"imagefield-field_meal_images"}):
			foodName = name.get('title')
			print(foodName)'''




#			for 
			#Food should be a list, first name then catagories
#			food = name.get('title')

#			allFoods[food] = []


#			food_list.append(food)


















		#print(aColumn)
		#columnData = soup.find("td",{aColumn}) 
		
		#print(type(columnData)) #This is a 'bs4.element.tag'
		#columnData = columnData.String
		#print(type(columnData))

		#print(columnData['class'])

		#Now just string searches?
		

		#print(name)


		#name = columnData.find('title')
		#name = columnData.find()
		#columnData.get('')
		#print(columnData)

#getTotalInfo()

