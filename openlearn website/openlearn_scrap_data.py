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



url="http://www.open.edu/openlearn/free-courses/full-catalogue"

course_link="http://www.open.edu"


workbook = xlsxwriter.Workbook('openlearn_all_courses.xlsx')
worksheet = workbook.add_worksheet()



# Open a workbook 
workbook1 = xlrd.open_workbook('openlearn_links.xlsx')  #collect all links from this file
worksheet1 = workbook1.sheet_by_name('Sheet1')
r=1
for row in range(1,924):#924
	course_url=worksheet1.cell(row,0).value
	worksheet.write_url(r,0,course_url)
	
	html=requests.get(course_url)
	course=BeautifulSoup(html.text,"lxml")
	
	try:
		title=course.find("h1",{"id":"aria-article-main-label"}).string
		#print(title.strip())
		worksheet.write(r,1,title.strip())
	except:
		worksheet.write(r,2,"None")
		
	try:
		try:
			image=course.find("div",{"class":"wall-image local-oucontentng-view"}).find("img")['src']
		except:
			image=course.find("div",{"class":"wall-image enrol-openlearn-enrolself"}).find("img")['src']
		#print(image)
		worksheet.write(r,2,image)
		alt=image.split("/")
		alt=alt[-1]
		#data = urllib.request.urlopen(image).read()
		#file = open("Images/"+str(alt), "wb")
		#file.write(data)
		#file.close()	
		worksheet.write_url(r,3,r"Images/"+str(alt))
	except:
		worksheet.write(r,3,"None")
	#print(course_url+"?active-tab=description-tab")
	#html1=requests.get("http://www.open.edu/openlearn/health-sports-psychology/question-ethics-right-or-wrong/content-section-0?active-tab=description-tab")
	#course1=BeautifulSoup(html1.text,"lxml")
	
	try:
		#link="http://www.open.edu/openlearn/health-sports-psychology/question-ethics-right-or-wrong/content-section-0"         #?active-tab=description-tab"
		browser = webdriver.Firefox()
		#print(course_url)
		browser.get(course_url)
		time.sleep(2)
		bond_source = browser.page_source
		#browser.quit()
		des=BeautifulSoup(bond_source,"lxml")
		
		browser.find_element_by_xpath("//h2[@id='content-tab']//a[@class='tab-link']").click()
		time.sleep(2)
		bond_source = browser.page_source
		#browser.quit()
		conn=BeautifulSoup(bond_source,"lxml")
		'''
		browser.find_element_by_xpath("//h2[@id='review-tab']//a[@class='tab-link']").click()
		try:
			pass#browser.find_element_by_xpath("//a[@class='comment_all button ou_silver']").click()
		except:
			pass
		bond_source = browser.page_source
		#browser.quit()
		reviews=BeautifulSoup(bond_source,"lxml")
		'''
		browser.quit()
	except KeyboardInterrupt:
		workbook.close()
		exit(0)
	except:
		pass
	#except:
	#	pass
	
	try:
		#print(course1)
		desc=des.find("div",{"id":"content_summary"}).find("p",{"property":"schema:description"}).string
		#print(str(desc))
		worksheet.write(r,4,desc.strip())
	except:
		worksheet.write(r,4,"None")
		
	try:
		outcomes=des.find("div",{"id":"summary_content"}).find("div",{"id":"blockoutcomes"}).find("ul").findAll("li")
		outcome=" "
		for each in outcomes:
			point=each.find("span",{"class":"content-list"}).string
			outcome+=point+", "
		#print(outcome)
		worksheet.write(r,5,outcome)
	except:
		worksheet.write(r,5,"None")
		
	try:
		contents=conn.find("ul",{"class":"accordionList"}).findAll("li",{"class":"accordionItem"})
		lists=" "
		for each in contents:
			data=each.find("span",{"class":"display-cell text-cell"}).find("span").string
			lists+=data+", "
		#print(lists)
		worksheet.write(r,6,lists)
	except:
		worksheet.write(r,6,"None")
	'''
	try:
		rev=reviews.find("div",{"class":"fivestar-summary fivestar-summary-combo"}).find("span",{"class":"average-rating"}).find("span").string
		rev=str(rev)+" / 5"
		print(str(rev))
		worksheet.write(r,7,rev)
	except KeyboardInterrupt:
		worksheet.write(r,7,"0")
	
	try:
		comment=" "
		comm_auth=reviews.findAll("div",{"class":"comment-author"})
		print((comm_auth))
		comm_data=reviews.findAll("div",{"class":"comment-content"})
		print((comm_data))
		for k in range(len(comm_data)):
			ee=comm_auth[k].find("a").string
			ww=comm_data[k].find("div",{"class":"field-item even"}).find("p").string
			comment+="< "+ee+" : "+ww+" >"
			print(comment)
		worksheet.write(r,8,comment)
	except KeyboardInterrupt:
		worksheet.write(r,8,"None")
	'''
	
	hrs=worksheet1.cell(row,1).value
	worksheet.write(r,7,hrs)
	
	
	level=worksheet1.cell(row,2).value
	worksheet.write(r,8,level)
	
	try:
		rat=conn.find("div",{"id":"about_free_course"}).find("div",{"class":"creative-commons border-solid"}).find("div",{"class":"course-info fivestar-value"}).find("span",{"class":"average-value"}).string
		rat=str(rat)+" / 5"
		#print(rat)
		worksheet.write(r,9,rat)
	except:
		worksheet.write(r,9,"0 / 5")
	
	try:
		enroll=course.find("a",{"title":"Create an account"})['href']
		#print(enroll)
		worksheet.write_url(r,10,enroll)
	except:
		worksheet.write(r,10,"None")
	
	
	try:
		subject=course.find("span",{"class":"subject-name"}).string
		#print(subject)
		worksheet.write(r,11,subject)
	except:
		worksheet.write(r,11,"None")
	
	
	try:
		w=12
		#download=conn.find("div",{"class":"block-download-course block-sidebar color-royal-blue"}).find("ul").findAll("li")
		download=conn.find("div",{"id":"sidebar_wrapper"}).find("ul").findAll("li")
		for each in download:
			pdf=each.find("a")['href']
			worksheet.write_url(r,w,pdf)
			w=w+1
	except:
		worksheet.write(r,w,"None")
	
	
	print(r)
	r=r+1
	#break
workbook.close()