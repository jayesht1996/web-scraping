
from bs4 import BeautifulSoup
import requests
import xlwt
import xlrd
import urllib.request as ur
import urllib
import re,os
from urllib.request import urlopen
import xlsxwriter,xlrd,time
from os import listdir
from os.path import isfile, join
import json

# Open a workbook 
#workbook = xlrd.open_workbook('study_all_courses.xlsx')  #collect all links from this file
#worksheet = workbook.sheet_by_name('Sheet1')

# Retrieve the value from cell at indices (0,0) 
#p=worksheet.cell(1, 1).value
#print(p)

course_link="http://www.canvas.net"
workbook1 = xlsxwriter.Workbook('canvas_all_json1.xlsx')
worksheet1 = workbook1.add_worksheet()
f=1
p=1
img=[]
while f<=7:
	url="https://www.canvas.net/products.json?page="+str(f)
	jsondata = requests.get(url).json()
	f=f+1
	#print(jsondata)
	#courses=BeautifulSoup(html.text,"lxml")
	data=jsondata['products']
	

	
	for row in data:
		link=row['url']
		#page=course_link+link
		worksheet1.write_url(p,0,link)
		title=row['title']
		worksheet1.write(p,1,title)
		teaser=row['teaser']
		worksheet1.write(p,2,teaser)
		price=row['priceWithCurrency']
		worksheet1.write(p,3,price)
		image=row['image']
		#image=course_link+image
		#print(image)
		img.append(image)
		worksheet1.write_url(p,4,image)
		logo_url=row['logo']['url']
		worksheet1.write_url(p,5,logo_url)
		logo_label=row['logo']['label']
		worksheet1.write(p,6,logo_label)
		free=row['free']
		worksheet1.write(p,7,free)
		publish=row['date']
		#date=str(time.ctime(publish/1000))
		worksheet1.write(p,8,publish)
		id=row['id']
		worksheet1.write(p,9,id)
		credits=str(row['credits'])
		worksheet1.write(p,10,credits)
		
		p=p+1
		print(p)

print(len(img))
print(len(set(img)))
