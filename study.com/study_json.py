
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
url="http://study.com/academy/course/prongs.ajax?limit=10000&offset=0"

course_link="http://www.study.com"
workbook1 = xlsxwriter.Workbook('study_all_json.xlsx')
worksheet1 = workbook1.add_worksheet()


jsondata = requests.get(url).json()

#print(jsondata)
#courses=BeautifulSoup(html.text,"lxml")
data=[]

p=1
for row in jsondata:
	link=row['uri']
	page=course_link+link
	worksheet1.write_url(p,0,page)
	title=row['title']
	worksheet1.write(p,1,title)
	view=row['popularity']
	worksheet1.write(p,2,view)
	lesson=row['lessonCount']
	worksheet1.write(p,3,lesson)
	image=row['imageUriLarge']
	image=course_link+image
	data.append(image)
	worksheet1.write_url(p,4,image)
	path=row['pathType']
	worksheet1.write(p,5,path)
	up=row['thumbsUp']
	worksheet1.write(p,6,up)
	down=row['thumbsDown']
	worksheet1.write(p,7,down)
	publish=row['datePublished']
	date=str(time.ctime(publish/1000))
	worksheet1.write(p,8,date)
	resourse=row['resourceName']
	worksheet1.write(p,9,resourse)
	research=row['isResearchArticleBundle']
	worksheet1.write(p,10,research)
	exam=row['examPath']
	exam=course_link+exam
	worksheet1.write_url(p,11,exam)
	p=p+1
print(p)

print(len(data))
print(len(set(data)))
