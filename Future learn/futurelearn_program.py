
from bs4 import BeautifulSoup
import requests,re
import csv,xlsxwriter
import os,urllib

print("start")
courses_link="https://www.futurelearn.com/programs"
html=requests.get(courses_link)

workbook = xlsxwriter.Workbook('future_learn_program.xlsx')
worksheet = workbook.add_worksheet()


courses=BeautifulSoup(html.text,'lxml')

course_url="https://www.futurelearn.com"

links=courses.find("ul",{"class":"m-grid-large"}).findAll("li",{"class":"m-grid-large__col"})#

url=[]
for row in links:
	url.append(row.find("a",{"class":"link-block"})['href'])

print(url)
print(len(url))

university=courses.findAll("div",{"class":"o-signpost__label"})
print(university[0].string)

intro=courses.findAll("div",{"class":"o-signpost__intro"})
print(intro[0].string)


info=courses.findAll("div",{"class":"o-signpost__info"})
print(info[0].find("span").string)


p=0
worksheet.write(p,0,"Program Url")
worksheet.write(p,1,"Title")
worksheet.write(p,2,"Enroll Url")
worksheet.write(p,3,"University")
#worksheet.write(p,4,"Number of course")
worksheet.write(p,5,"Information")
worksheet.write(p,6,"Introduction")
worksheet.write(p,7,"Course Url")

p=1

for ret in range(0,len(url)):
	print(course_url+url[ret])
	
	
	try:
		worksheet.write(p,3,university[ret].string)
	except:
		worksheet.write(p,3,"None")
	
	try:
		worksheet.write(p,6,intro[ret].string)
	except:
		worksheet.write(p,6,"None")
	
	try:
		worksheet.write(p,5,info[ret].find("span").string)
	except:
		worksheet.write(p,5,"None")
	
	topic_courses=requests.get(course_url+url[ret])
	course=BeautifulSoup(topic_courses.text,'lxml')
	
	
	try:
		title=course.find("div",{"class":"m-banner--header__title"}).find("h1").string
		worksheet.write(p,1,title)
	except:
		worksheet.write(p,1,"None")
		
	num_course=[]
	try:
		num_course=course.find("div",{"class":"a-content a-content--tight-top"}).find("ul",{"class":"run-list"})
		num=num_course.findAll("a",{"class":"m-course-run__media media-zoom "})#['href']
		#print(num)
		#worksheet.write(p,4,len(num))
	except:
		#worksheet.write(p,4,"None")
		
	try:
		join=course.find("div",{"class":"m-banner--header__cta--wrapper section-cta--after-copy"}).find("form")['action']
		worksheet.write_url(p,2,course_url+join)
	except:
		worksheet.write_url(p,2,"None")
	
		
	try:
		worksheet.write_url(p,0,course_url+url[ret])
	except:
		worksheet.write_url(p,0,"None")
	
	w=7
	try:
		for row in num:
			print(row)
			courses_prog=row['href']
			#print(courses_prog)
			
			worksheet.write_url(p,w,course_url+courses_prog)
			w=w+1
	except:
		worksheet.write(p,w,"None")
			
	p=p+1
	
workbook.close()