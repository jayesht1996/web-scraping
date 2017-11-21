from bs4 import BeautifulSoup
import requests
import xlwt
import xlrd
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




# Open a workbook 
workbook1 = xlrd.open_workbook('canvas_all_json.xlsx')  #collect all links from this file
worksheet1 = workbook1.sheet_by_name('Sheet1')


workbook = xlsxwriter.Workbook('canvas_all_courses.xlsx')
worksheet = workbook.add_worksheet()

course_link="http://www.canvas.net"
add=0
r=1


for row in range(1,125):
	link=worksheet1.cell(row, 0).value
	html=requests.get(link)
	course=BeautifulSoup(html.text,"lxml")
	worksheet.write_url(r,0,link)
	
	title=worksheet1.cell(row, 1).value
	worksheet.write(r,1,title)
	
	desc=worksheet1.cell(row, 2).value
	worksheet.write(r,2,desc)
	
	
	image=worksheet1.cell(row, 4).value
	image=image.split("?")
	image=image[0]
	alt=image.split("/")
	alt=alt[-1]
	data = urllib.request.urlopen(image).read()
	file = open("Cover/"+str(alt), "wb")
	file.write(data)
	file.close()	
	worksheet.write_url(r,4,image)
	worksheet.write_url(r,3,r"Cover/"+str(alt))
	
		
	university=worksheet1.cell(row, 6).value
	worksheet.write(r,5,university)
	
	logo=worksheet1.cell(row, 5).value
	logo=logo.split("?")
	logo=logo[0]
	alt=logo.split("/")
	alt=alt[-1]
	data = urllib.request.urlopen(image).read()
	file = open("Logo/"+str(alt), "wb")
	file.write(data)
	file.close()	
	worksheet.write_url(r,7,logo)
	worksheet.write_url(r,6,r"Logo/"+str(alt))
	
	price=worksheet1.cell(row, 3).value
	worksheet.write(r,8,price)
	
	free=worksheet1.cell(row, 7).value
	if free==True:
		val="Yes"
	else:
		val="No"
	#print(val)
	worksheet.write(r,9,val)
	
	date=worksheet1.cell(row, 8).value
	worksheet.write(r,10,date)
	
	try:
		duration=course.find("div",{"class":"detail-duration"}).find("p").string
		worksheet.write(r,11,duration)
	except:
		worksheet.write(r,11,"None")
		
	try:
		comm=course.find("div",{"class":"detail-commitment"}).find("p").string
		worksheet.write(r,12,comm)
	except:
		worksheet.write(r,12,"None")
		
	try:
		reqr=course.find("div",{"class":"detail-requirement"}).find("p").string
		worksheet.write(r,13,reqr)
	except:
		worksheet.write(r,13,"None")
		
	try:
		type=course.find("div",{"class":"detail-type"}).find("p").string
		worksheet.write(r,14,type)
	except:
		worksheet.write(r,14,"None")
	
	try:
		cre=course.find("div",{"class":"detail-credential"}).find("p").string
		worksheet.write(r,15,cre)
	except:
		worksheet.write(r,15,cre)
	
	try:
		object=""
		obj=course.find("div",{"class":"course-information dk"}).find("div",{"class":"main-column col-md-8"}).find("ul").findAll("li")
		for each in obj:
			object+=each.string+"  "
		worksheet.write(r,16,object)
	except:
		worksheet.write(r,16,"None")
	
	
	id=int(worksheet1.cell(row, 9).value)
	worksheet.write(r,17,id)
	
	
	try:
		#enroll=course.find("div",{"class":"product-image"})#.find("a")['href']
		enroll="https://www.canvas.net/courses/"+str(id)+"/enrollment/new"
		#print(str(enroll))
		worksheet.write(r,18,enroll)
	except KeyboardInterrupt:
		worksheet.write(r,18,"None")
		
	
	
	try:
		browser = webdriver.Firefox()
		browser.get(link)
		bond_source = browser.page_source
		browser.quit()
		soup = BeautifulSoup(bond_source,"lxml")
		diff=soup.find("div",{"class":"side-column col-md-4"}).findAll("iframe")#['src']
		
		tt=diff[-1]['src']
		#print(tt)
		html2=requests.get(tt)
		next=BeautifulSoup(html2.text,"lxml")
		#print(next)
	except KeyboardInterrupt:
		workbook.close()
		exit(0)
	except:
		pass
	#break
	
	try:
		#rev=soup.find("header",{"class":"widgetHeader"})#.find("h1",{"class":"widgetTitle"}).find("span",{"class":"widgetTitle_count"})#.string
		#rev=course.find("a",{"class":"widgetTitleLink"})#.find("h1",{"class":"widgetTitle"}).find("span",{"class":"widgetTitle_count"}).string
		rev=next.find("span",{"class":"widgetTitle_count"}).string
		#print(str(rev))
		worksheet.write(r,19,rev)
		#print(rev)
	except:
		worksheet.write(r,19,"None")
	#break
	try:
		ret=next.find("div",{"class":"widgetFooter_layoutUnit widgetFooter_layoutUnit-right"}).find("a")['href']
		#print(ret)
		ret="https://www.class-central.com"+ret
		html1=requests.get(ret)
		review=BeautifulSoup(html1.text,"lxml")
	
		try:
			all=review.find("div",{"class":"course-all-reviews"}).findAll("div",{"class":"single-review"})
			all_review=""
			for each in all:
				author=each.find("span",{"class":"author"}).string
				rev_prev=each.find("div",{"class":"review-full"})#.string
				#rev_prev=str(rev_prev).split(">")
				#rev_prev=str(rev_prev[1]).split("<")
				rev_prev=str(rev_prev).replace('<div class="review-full">','')
				rev_prev=str(rev_prev).replace('</div>','')
				rev_prev=str(rev_prev).replace("<br>","")
				rev_prev=str(rev_prev).replace("</br>","")
				rev_prev=str(rev_prev).replace("<br/>","")
				rev_prev=str(rev_prev).replace("\n","")
				
				#rev_prev=str(rev_prev).replace("<br>","")
				#print(author)
				#print(rev_prev)
				all_review+="< "+author+" : "+rev_prev+" >"
				#print(all_review)
			worksheet.write(r,20,all_review)
		except:
			worksheet.write(r,20,"None")
	except:
		worksheet.write(r,20,"None")
		
		
	w=21
	try:
		ins=course.find("div",{"class":"instructor-info"}).findAll("div",{"class":"instructor-container"})
		for each in ins:
			try:
				image=each.find("img")['src']
				alt=image.split("/")
				alt=alt[-1]
				data = urllib.request.urlopen(image).read()
				file = open("Instructor/"+str(alt), "wb")
				file.write(data)
				file.close()	
				worksheet.write_url(r,w,image)
			except:
				worksheet.write(r,w,"None")
			w=w+1
			try:
				worksheet.write_url(r,w,r"Instructor/"+str(alt))
			except:
				worksheet.write(r,w,"None")
			w=w+1
			try:
				ins_name=each.find("div",{"class":"instructor-name"}).find("h4").string
				worksheet.write(r,w,ins_name)
			except:
				worksheet.write(r,w,"None")
			w=w+1
			try:
				ins_bio=""
				ins_bio=each.find("div",{"class":"instructor-bio"}).find("p")
				#print(str(ins_bio))
				ins_bio=str(ins_bio).split("<span")
				ins_bio=ins_bio[0]
				ins_bio=ins_bio[3:]+"  "
				#print(ins_bio)
				ins_bio+=each.find("div",{"class":"instructor-bio"}).find("div",{"class":"more-text"}).find("p").string
				#print(ins_bio)
				worksheet.write(r,w,ins_bio)
			except:
				worksheet.write(r,w,"None")
			w=w+1
	except:
		worksheet.write(r,w,"None")
			
	print(r)
	r=r+1
	
	
workbook.close()
