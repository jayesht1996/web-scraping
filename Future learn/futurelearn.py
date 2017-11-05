
from bs4 import BeautifulSoup
import requests,re
import csv,xlsxwriter
import os,urllib

print("start")
courses_link="https://www.futurelearn.com/courses?filter_availability=open"
html=requests.get(courses_link)

workbook = xlsxwriter.Workbook('future_learn_course4.xlsx')
worksheet = workbook.add_worksheet()

p=0
worksheet.write(p,0,"Title")
worksheet.write(p,1,"Description")
worksheet.write(p,2,"University")
worksheet.write(p,3,"Image Url")
worksheet.write(p,4,"Logo")
worksheet.write(p,5,"Learn")
worksheet.write(p,6,"Available")
worksheet.write(p,7,"Join link")
worksheet.write(p,8,"Achive")
worksheet.write(p,9,"Course_for")
worksheet.write(p,10,"Instructor Image")
worksheet.write(p,11,"Instructor Name")
worksheet.write(p,12,"Instructor Details")
worksheet.write(p,13,"Total Time")
worksheet.write(p,14,"Week time")
worksheet.write(p,15,"Video url")
worksheet.write(p,16,"Course url")





courses=BeautifulSoup(html.text,'lxml')
print("hey")
course_url="https://www.futurelearn.com"


links = courses.find("div",{"class":"m-filter__content"}).find("div", {"class" : "m-grid-of-cards m-grid-of-cards--compact"})
print("link"+str(len(links)))
url=links.findAll("a")#['href']
print(len(url))
#print(url[0].find("img")["src"])

#print(str(url[0]))
images=[]
urls=[]
for i in url:
	images.append(i.find("img")["src"])
	hr=str(i).split('href="')
	lin=hr[1].split('"')
	urls.append(lin[0])
	
#print(images)
#print(urls)
print(len(urls))


university = courses.findAll("div", { "class" : "a-item-title a-item-title--secondary a-item-title--light" })
print(len(university))
print(university[0].string)

title = courses.findAll("div", { "class" : "m-new-card__title" })
print(len(title))
print(title[0].string)

desc = courses.findAll("div", { "class" : "m-new-card__intro" })

print(len(desc))
print(desc[0].string)

total_time = courses.findAll("span", { "class" : "m-new-card__metadata-label" })
print(len(total_time))
print(total_time[0].string)

r=0
p=1
for ret in range(350,len(title)):
	try:
		print(p)
		topic_link=urls[ret]
		temp=[]
		ins=[]
		#print(i)
		#print(topic_link)
		topic_courses=requests.get(course_url+topic_link)
		print(course_url+topic_link)
		course=BeautifulSoup(topic_courses.text,'lxml')
	except:
		continue
	try:
		worksheet.write(p,0,title[ret].string)
	except:
		worksheet.write(p,0,"None")
	
	try:
		worksheet.write(p,1,desc[ret].string)
	except:
		worksheet.write(p,1,"None")
	
	try:
		worksheet.write(p,2,university[ret].string)
	except:
		worksheet.write(p,2,"None")
	
	try:		
		alt=images[ret].split(".svg")
		alt=alt[0]
		#alt=alt+".jpg"
		print(alt)
		alt=alt.split("/")
		alt=alt[-1]
		data = urllib.request.urlopen(images[ret]).read()
		file = open("Images/"+str(alt), "wb")
		file.write(data)
		file.close()	
		worksheet.write_url(p,3,r"Images/"+str(alt))
	except:
		worksheet.write(p,3,"None")
		
	try:		
		logo=course.find("div",{"class":"a-standard-org-logo"}).find("a").find("img")['src']
		print("Logo:-"+str(logo))
		#alt1=logo.split(".svg")
		#alt1=alt1[0]
		#alt1=alt1+".jpg"
		
		
		alt1=logo.split("/")
		alt1=alt1[-1]
		data = urllib.request.urlopen(logo).read()
		file = open("Logo/"+str(alt1), "wb")
		file.write(data)
		file.close()
		worksheet.write_url(p,4,r"Logo/"+str(alt1))
	except:
		worksheet.write(p,4,"None")

	try:
		learn_data=""
		learn=course.find("section",{"id":"section-topics"}).find("div",{"class":"a-text-context"}).find("ul").findAll("li")
		for m in learn:
			le=m.string
			#print(le)
			learn_data=learn_data+str(le)
		#print(learn)
		print(learn_data)
		worksheet.write(p,5,learn_data)
	except:
		worksheet.write(p,5,"None")

	try:
		available="No"
		available=course.find("li",{"class":"m-shelved-table__shelve"}).find("div",{"class":"m-shelved-table__message"}).string
		print("str"+str(available))
		if "Available now" not in available:
			available=course.find("li",{"class":"m-shelved-table__shelve"}).find("ul",{"class":"m-shelved-table"}).find("time").string
			print(available)
		else:
			available="Yes"
		print(available)
		worksheet.write(p,6,available)
	except:
		worksheet.write(p,6,"None")
		
	try:		
		try:
			join=course.find("li",{"class":"m-shelved-table__shelve"}).find("div",{"class":"m-shelved-table__cta"}).find("a")['href']
			#join=course.find("li",{"class":"m-shelved-table__shelve"}).find("div",{"class":"m-shelved-table__cta"}).find("form")['action']
			#print(course_url+join)
		except:
			join=course.find("li",{"class":"m-shelved-table__shelve"}).find("div",{"class":"m-shelved-table__cta"}).find("form")['action']
			#join=course.find("li",{"class":"m-shelved-table__shelve"}).find("div",{"class":"m-shelved-table__cta"}).find("a")['href']
			#print(course_url+join)
		worksheet.write_url(p,7,course_url+join)
	except:
		worksheet.write_url(p,7,"None")
		
	try:	
		achive=""

		what_achive=course.find("div",{"class":"a-content a-content--contiguous-bottom a-content--tight-top a-content--mega"}).find("ul").findAll("li")
		print(what_achive)
		for i in what_achive:
			ach=i.find("div").string
			print(ach)
			achive=achive+ach
			
		print(achive)
		worksheet.write(p,8,achive)
	except:
		worksheet.write(p,8,"None")
		
		
	try:
		course_for=course.find("section",{"id":"section-requirements"}).find("div",{"class":"a-text-context"}).find("p").string
		print("this course is for")
		print(course_for)
		worksheet.write(p,9,course_for)
	except:
		worksheet.write(p,9,"None")
		
	
		
	#no_ins=course.findAll("div",{"class":"m-grid-educators"})
	ins_detail=""
	ins_name=""
	
	try:
		#for i in range(len(no_ins)):
		ins_image=course.find("div",{"class":"m-grid-educators"}).find("div",{"class":"m-media-element__image"}).find("a").find("img")['src']
		
		#alt=alt+".jpg"
		print(ins_image)
		alt=ins_image.split("/")
		alt=alt[-1]
		data = urllib.request.urlopen(ins_image).read()
		file = open("Instructor_images/"+str(alt), "wb")
		file.write(data)
		file.close()	
		worksheet.write_url(p,10,r"Instructor_images/"+str(alt))
	except:
		worksheet.write_url(p,10,"None")
	
	try:
		ins_nam=course.find("div",{"class":"m-grid-educators"}).find("header",{"class":"m-info-block__header m-info-block__header--double"}).find("h3").find("a").string
		#print(ins_nam)
		ins_name+=ins_nam
		worksheet.write(p,11,ins_name)
	except:
		worksheet.write(p,11,"None")
	
	try:
		ins_det=course.find("div",{"class":"m-grid-educators"}).find("div",{"class":"m-info-block__body"}).find("p").string
		#print(ins_det)
		ins_detail+=ins_det
		worksheet.write(p,12,ins_detail)
	except:
		worksheet.write(p,12,"None")
	
	try:
		worksheet.write(p,13,total_time[r].string)
		r=r+1
	except:
		worksheet.write(p,13,"None")
	
	try:
		worksheet.write(p,14,total_time[r].string)
		r=r+1
	except:
		worksheet.write(p,14,"None")
		
	try:
		video=course.find("div",{"class":"video-options__video"}).find("a")['href']
		video="http:"+video
		print(video)
		alt1=video.split("/")
		alt1=alt1[-1]+str(ret)+".mp4"
		print(alt1)
		data = urllib.request.urlopen(video).read()
		print("hii")
		file = open("Video/"+str(alt1), "wb")
		file.write(data)
		file.close()
		worksheet.write_url(p,15,r"Video/"+str(alt1))
	except:
		worksheet.write(p,15,"None")

	try:
		worksheet.write_url(p,16,course_url+topic_link)
	except:
		worksheet.write_url(p,16,"None")

	p=p+1
		
workbook.close()