
from bs4 import BeautifulSoup
import requests,re
import csv,xlsxwriter
import os,urllib

courses_link="https://www.futurelearn.com/degrees"
html=requests.get(courses_link)

workbook = xlsxwriter.Workbook('future_learn_degree1.xlsx')
worksheet = workbook.add_worksheet()


courses=BeautifulSoup(html.text,'lxml')

course_url="https://www.futurelearn.com"

links=courses.find("div",{"class":"m-grid-of-cards"})#.findAll("a",{"class":"link-block m-new-card"})
link=links.findAll("a")

print(link)
url=[]
for row in link:
	url.append(row['href'])

print(url)
print(len(url))

image_url=[]
image=courses.findAll("div",{"class":"m-new-card__image a-ribbon-container--campaign-grid"})

for row in image:
	image_url.append(row.find("img")['src'])
	
print(image_url)

titles=courses.findAll("div",{"class":"m-new-card__title"})


intro=courses.findAll("div",{"class":"m-new-card__intro"})


level=courses.findAll("div",{"class":"m-new-card__options m-new-card__degree-options"})

p=0
worksheet.write(p,0,"Course Url")
worksheet.write(p,1,"Title")
worksheet.write(p,2,"Image")
worksheet.write(p,3,"Level")
worksheet.write(p,4,"Introduction")
worksheet.write(p,5,"Apply now")
worksheet.write(p,6,"Apply Graduate Certificate")
worksheet.write(p,7,"Apply graduate diploma")
worksheet.write(p,8,"apply master degree")
worksheet.write(p,9,"Why to join")
worksheet.write(p,10,"Benefits")
worksheet.write(p,11,"Certificate program")
worksheet.write(p,12,"Diploma program")
worksheet.write(p,13,"Master program")


p=1
for ret in range(0,len(url)):
	print(course_url+url[ret])
	
	try:
		worksheet.write_url(p,0,course_url+url[ret])
	except:
		worksheet.write(p,0,"None")
	
	try:
		worksheet.write(p,4,intro[ret].string)
	except:
		worksheet.write(p,4,"None")
	
	try:
		worksheet.write(p,1,titles[ret].string)
	except:
		worksheet.write(p,1,"None")
	
	try:
		stri=""
		all=level[ret].findAll("p")
		for i in all:
			stri+=i.string+", "
		worksheet.write(p,3,stri)
	except:
		worksheet.write(p,3,"None")
	
	try:		
		alt=image_url[ret]
		alt=alt.split("/")
		alt=alt[-1]
		data = urllib.request.urlopen(image_url[ret]).read()
		file = open("Images/"+str(alt), "wb")
		file.write(data)
		file.close()	
		worksheet.write_url(p,2,r"Images/"+str(alt))
	except:
		worksheet.write(p,2,"None")
			
	
	
	
	topic_courses=requests.get(course_url+url[ret])
	course=BeautifulSoup(topic_courses.text,'lxml')
	
	
	try:
		apply=course.find("div",{"class":"m-button-group__primary"}).find("a")['href']
		print(apply)
		worksheet.write_url(p,5,course_url+apply)
	except:
		worksheet.write(p,5,"None")
		
	try:
		degree=requests.get(course_url+apply)#(course_url+url[ret])
		detail=BeautifulSoup(degree.text,'lxml')

		val=detail.find("div",{"class":"m-portfolio__list"}).findAll("a",{"class":"a-button a-button--elastic"})
		#print(val)
		data=[]
		for row in val:
			data.append(row['href'])
		#print(data)
	except:
		print("Error")
		
	try:
		worksheet.write_url(p,6,data[0])
	except:
		worksheet.write(p,6,"None")

	try:
		worksheet.write_url(p,7,data[1])
	except:
		worksheet.write(p,7,"None")

		
	try:
		worksheet.write_url(p,8,data[2])
	except:
		worksheet.write(p,8,"None")

		
	try:
		why_join=course.find("div",{"class":"a-content a-content--tight-top a-content--contiguous-bottom"}).find("div",{"class":"a-text-context"}).findAll("p")
		stri=""
		for row in why_join:
			stri+=row.string+". "
		worksheet.write(p,9,stri)
	except:
		worksheet.write(p,9,"None")

	try:
		benefits=course.find("ul",{"class":"m-list-grid"}).findAll("div",{"class":"m-list-with-icon__text"})
		stri=""
		for row in benefits:
			stri+=row.string+". "
		worksheet.write(p,10,stri)
	except:
		worksheet.write(p,10,"None")
		
	try:
		#certi=course.find("a",{"class":"js-drawer-toggle m-drawer-list__degree"}).findAll("span",{"class":"m-drawer-list__degree-type"})
		certi=course.findAll("span",{"class":"m-drawer-list__degree-type"})
		prog=course.find("div",{"class":"m-drawer-list m-drawer-list--open-if-no-js"}).findAll("ol",{"class":"m-drawer-list__programs"})
		print(certi)
		for j in certi:
			print(j)
			print(j.string)
		print(len(certi))
		#print(prog)
		w=11
		print(all)
		try:
			for i in range(len(certi)):
				stri=str(all[i].string)+" - "
				print(stri)
				pre=prog[i].findAll("li")
				#print(pre)
				for row in pre:
					stri=stri+str(row.find("p").string)+", "
				#print(stri)
				try:
					worksheet.write(p,w,stri)
				except:
					worksheet.write(p,w,"None")
					
				w+=1
		except Exception as e:
			print(e)
			pass
	except:
		pass
		
		
		
		
		
		
	p=p+1
	
workbook.close()