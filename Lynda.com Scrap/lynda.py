
from bs4 import BeautifulSoup
import requests
import csv,xlsxwriter
import os

courses_link="https://www.lynda.com/subject/all"
html=requests.get(courses_link)

courses=BeautifulSoup(html.text)

mydivs = courses.findAll("div", { "class" : "software-name" })

workbook = xlsxwriter.Workbook('lynda.xlsx')
worksheet = workbook.add_worksheet()

p=0
worksheet.write(p,0,"Title")
worksheet.write(p,1,"Instructor")
worksheet.write(p,2,"Course_link")
worksheet.write(p,3,"Duration")
worksheet.write(p,4,"Level")
worksheet.write(p,5,"Views")
worksheet.write(p,6,"Release date")
worksheet.write(p,7,"Description")

p=1
for i in mydivs:
	topic_link=i.find("a")["href"]
	topic_courses=requests.get(courses_link+topic_link)

	course=BeautifulSoup(topic_courses.text)
	all_courses=course.findAll("div", { "class" : "col-xs-8 col-sm-9 card-meta-data" })

	for c in all_courses:
		try:
			course_link=c.find('a')['href']
			title=c.find('h3').string
			inst=c.find("div", {"class":"title-author-info"})
			instr=inst.find("cite",{"class":"meta-author"}).string
			desc=inst.find("div",{"class":"meta-description"}).string
			meta=c.find("div", {"class":"meta"})
			duration=meta.find("span",{"class":"meta-duration"}).string
			level=meta.find("span",{"class":"meta-level"}).string
			views=meta.find("span",{"class":"meta-views"}).find('span').string
			release_date=meta.find("span",{"class":"meta-released"}).find('span').string
		 
			#print(course_link)
			worksheet.write(p,0,title)
			worksheet.write(p,1,instr)
			worksheet.write(p,2,course_link)
			worksheet.write(p,3,duration)
			worksheet.write(p,4,level)
			worksheet.write(p,5,views)
			worksheet.write(p,6,release_date)
			worksheet.write(p,7,desc)
		except:
			continue
		print(p)
		p=p+1

workbook.close()
