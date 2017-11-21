from bs4 import BeautifulSoup
import requests
import urllib.request as ur
import urllib
import re,os,time
from urllib.request import urlopen
import xlsxwriter,xlrd
from os import listdir
from os.path import isfile, join
from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys



url="http://oyc.yale.edu/courses"

course_link="http://oyc.yale.edu"



workbook = xlsxwriter.Workbook('oyc_courses.xlsx')
worksheet = workbook.add_worksheet()



# Open a workbook 
workbook1 = xlrd.open_workbook('oyc_links1.xlsx')  #collect all links from this file
worksheet1 = workbook1.sheet_by_name('Sheet1')
r=1
for row in range(0,40):#40


	dept_url=worksheet1.cell(row,0).value
	worksheet.write_url(r,0,dept_url)
	
	html=requests.get(dept_url)
	dept=BeautifulSoup(html.text,"lxml")
	
	
	depart=worksheet1.cell(row,1).value
	worksheet.write(r,1,depart)
	
	
	desc=dept.find("div",{"class":"field field-name-body field-type-text-with-summary field-label-hidden"}).find("div",{"class":"field-item even"}).find("p")#.string
	desc=str(desc).split("<p>")
	desc=str(desc[1]).split("<a")
	desc=desc[0]
	#print(desc)
	worksheet.write(r,2,desc)
	
	depart_link=dept.find("div",{"class":"field field-name-body field-type-text-with-summary field-label-hidden"}).find("div",{"class":"field-item even"}).find("p").find("a")['href']
	#print(depart_link)
	worksheet.write_url(r,3,depart_link)
	

	course_url=worksheet1.cell(row,6).value
	worksheet.write_url(r,4,course_url)
	
	html=requests.get(course_url)
	course=BeautifulSoup(html.text,"lxml")
	
	
	no=worksheet1.cell(row,2).value
	worksheet.write(r,5,no)
	
	
	title=worksheet1.cell(row,3).value
	worksheet.write(r,6,title)
	
	date=worksheet1.cell(row,5).value
	worksheet.write(r,7,date)
	
	ins=worksheet1.cell(row,4).value
	worksheet.write(r,8,ins)

	try:
		ins_image=course.find("div",{"class":"views-field views-field-field-course-header-image"}).find("img")['src']
		worksheet.write_url(r,9,ins_image)
		#print(ins_image)
		
		alt=ins_image.split("/")
		alt=alt[-1]
	
		data = urllib.request.urlopen(ins_image).read()
		file = open("Images/"+str(alt), "wb")
		file.write(data)
		file.close()	
		worksheet.write_url(r,10,r"Images/"+str(alt))
	except:
		worksheet.write(r,10,"None")
	
	try:
		ins_descs=course.find("div",{"class":"views-field views-field-field-about-the-professor"}).findAll("p")
		ins_desc=" "
		for each in ins_descs:
			ins_desc+=str(each)
			
		ins_desc=ins_desc.replace("<p>","")
		ins_desc=ins_desc.replace("</p>","")
		ins_desc=ins_desc.replace("<em>","")
		ins_desc=ins_desc.replace("</em>","")
		ins_desc=ins_desc.split("<a")
		ins_desc=ins_desc[0]
		#print(ins_desc)
		worksheet.write(r,11,ins_desc)
	except:
		worksheet.write(r,11,"None")
		
	try:
		about=course.find("div",{"class":"views-field views-field-body"}).findAll("p")
		course_about=""
		for each in about:
			course_about+=each.string
		#print(course_about)
		worksheet.write(r,12,course_about)
	except:
		worksheet.write(r,12,"None")
	
	try:
		stru=course.find("div",{"class":"views-field views-field-field-course-structure"}).find("div",{"class":"field-content"}).string
		#print(stru)
		worksheet.write(r,13,stru)
	except:
		worksheet.write(r,13,"None")
	
	try:
		material=course.find("div",{"class":"views-row views-row-1 views-row-odd views-row-first views-row-last"}).find("div",{"class":"views-field views-field-field-course-download-link"}).find("div",{"class":"field-content"}).find("a")['href']
		#print(str(material))
		worksheet.write_url(r,14,material)
	except:
		worksheet.write(r,14,"None")
	
	try:
		texts=course.find("div",{"class":"views-field views-field-field-syllabus-texts"}).find("div",{"class":"field-content"}).findAll("p")
		text=""
		for each in texts:
			text+=str(each)
			
		text=text.replace("<p>","")
		text=text.replace("</p>","")
		text=text.replace("<em>","")
		text=text.replace("</em>","")
		text=text.replace("</span>","")
		text=text.replace("<span>","")
		text=text.replace("</strong>","")
		text=text.replace("<strong>","")
		text=text.replace("<a>","")
		text=text.replace("</a>","")
		#print(text)
		worksheet.write(r,15,text)
	except:
		worksheet.write(r,15,"None")
	
	try:
		reqrs=course.find("div",{"class":"views-field views-field-field-syllabus-requirements"}).find("div",{"class":"field-content"}).findAll("p")
		text=""
		for each in reqrs:
			text+=str(each)
			
		text=text.replace("<p>","")
		text=text.replace("</p>","")
		text=text.replace("<em>","")
		text=text.replace("</em>","")
		text=text.replace("</span>","")
		text=text.replace("<span>","")
		text=text.replace("</strong>","")
		text=text.replace("<strong>","")
		text=text.replace("<a>","")
		text=text.replace("</a>","")
		#print(text)
		worksheet.write(r,16,text)
	except:
		worksheet.write(r,16,"None")
	
	try:
		greds=course.find("div",{"class":"views-field views-field-field-syllabus-grading"}).find("div",{"class":"field-content"}).findAll("p")
		text=""
		for each in greds:
			text+=str(each)
			
		text=text.replace("<p>","")
		text=text.replace("</p>","")
		text=text.replace("<em>","")
		text=text.replace("</em>","")
		text=text.replace("</span>","")
		text=text.replace("<span>","")
		text=text.replace("</strong>","")
		text=text.replace("<strong>","")
		text=text.replace("<a>","")
		text=text.replace("</a>","")
		#print(text)
		worksheet.write(r,17,text)
	except:
		worksheet.write(r,17,"None")
	
	try:
		lectures=course.find("div",{"id":"quicktabs-tabpage-course-2"}).find("div",{"class":"view-content"}).find("tbody").findAll("tr")
		text=""
		for each in lectures:
			text+=each.find("td",{"class":"views-field views-field-field-session-display-title"}).find("a").string+", "
			
		text=text.replace("<p>","")
		text=text.replace("</p>","")
		text=text.replace("<em>","")
		text=text.replace("</em>","")
		text=text.replace("</span>","")
		text=text.replace("<span>","")
		text=text.replace("</strong>","")
		text=text.replace("<strong>","")
		text=text.replace("<a>","")
		text=text.replace("</a>","")
		#print(text)
		worksheet.write(r,18,text)
	except:
		worksheet.write(r,18,"None")
	
	
	try:
		survey=course.find("div",{"class":"views-field views-field-field-survey-link"}).find("div",{"class":"field-content"}).find("a")['href']
		#print(str(survey))
		worksheet.write_url(r,19,survey)
	except:
		worksheet.write(r,19,"None")
	
	try:
		books=course.find("div",{"class":"views-field views-field-field-books-link"}).find("div",{"class":"field-content"}).find("a")['href']
		#print(str(books))
		worksheet.write_url(r,20,books)
	except:
		worksheet.write(r,20,"None")
	
	print(r)
	r+=1
	
workbook.close()