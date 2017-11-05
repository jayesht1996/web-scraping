
from bs4 import BeautifulSoup
import requests,re
import csv,xlsxwriter
import os,urllib

courses_link="https://ocw.mit.edu/courses/index.htm"
html=requests.get(courses_link)

courses=BeautifulSoup(html.text)

course_url="https://ocw.mit.edu"
odd = courses.findAll("tr", { "class" : "odd" })
even = courses.findAll("tr", { "class" : "even" })
print(len(odd))
print(len(even))
workbook = xlsxwriter.Workbook('ocw_mit_even3.xlsx')
worksheet = workbook.add_worksheet()

p=0
worksheet.write(p,0,"Title")
worksheet.write(p,1,"Mit Number")
worksheet.write(p,2,"Category")
worksheet.write(p,3,"Level")
worksheet.write(p,4,"Image")
worksheet.write(p,5,"Instructor")
worksheet.write(p,6,"As Taught In")
worksheet.write(p,7,"Features")
worksheet.write(p,8,"Description")
worksheet.write(p,9,"Course Link")


p=1
w=1
for ret in range(1165,len(even)):#180
	try:
		i=even[ret]
		#print(i)
		temp=[]
		ins=[]
		#print(i)
		topic_link=i.find("td").find("a")["href"]
		#print(topic_link)
		number=i.find("td").find("a").string.strip()
		#print(number)
		topic_courses=requests.get(course_url+topic_link)

		course=BeautifulSoup(topic_courses.text,'lxml')

		course_info=course.find("div", {"id":"course_info"})

		title=course.find("h1", {"class":"title"}).string
		#print(title)
		category=course.find("nav", {"id":"breadcrumb_chp"}).find("p").findAll("a")
		cat=category[2].string
		#print(category)
		#print(cat)
		instructor=course_info.findAll("p", {"class":"ins"})
		for each in instructor:
			ins.append(each.string)
		#print(ins)
		date=course_info.find("p", {"itemprop":"startDate"}).string
		#print(date)
		level=course_info.find("p", {"itemprop":"typicalAgeRange"}).string
		#print(level)

		fea=[]
		course_desc=course.find("div", {"id":"description"})
		features=course_desc.find("ul", {"class":"specialfeatures"}).findAll("li")
		for each in features:
			fea.append(each.string)
		#print(fea)
		des=course_desc.find("p").string#, {"id":"description"})
		#print(des)

		image=course.find("div", {"class":"image"}).find("img")['src']
		#print(course_url+image)
		alt=image.split("/")
		alt=alt[-1]
		data = urllib.request.urlopen(course_url+image).read()
		file = open("Images/"+str(alt), "wb")
		file.write(data)
		file.close()	

		worksheet.write(p,0,title)
		worksheet.write(p,1,number)
		worksheet.write(p,2,cat)
		worksheet.write(p,3,level)
		worksheet.write_url(p,4,r"Images/"+str(alt))
		worksheet.write(p,5,str(', '.join(ins)))
		worksheet.write(p,6,date)
		worksheet.write(p,7,str(', '.join(fea)))
		worksheet.write(p,8,des)
		worksheet.write_url(p,9,course_url+topic_link)
		p+=1
		print(p)
	except KeyboardInterrupt:
		workbook.close()
		break
	except Exception as e:
		print(e)
		p=p+1
		continue
		
workbook.close()
		
		
		
		
'''
				
				
				
	all_images=course.findAll("div", { "class" : "col-xs-4 col-sm-3 image-column" })
    #print(all_images)
	for i in all_images:
		all_image=i.find("img")['data-lazy-src']
		alt=i.find("img")['alt']
		alt=alt.replace(" ","_")
		alt=alt.replace(":","")
		alt=alt.replace("?","")
		alt=alt.replace("&","")
		if re.findall('[^A-Za-z0-9]',alt):
			alt=''.join(e for e in alt if e.isalnum() or e=="_")
		alt=alt+".jpg"
		print(alt)
		course_img=all_image
		print(course_img)
		data = urllib.request.urlopen(course_img).read()
		file = open("Images/"+str(alt), "wb")
		file.write(data)
		file.close()
		worksheet.write_url(w,8,r"Images/"+str(alt))
		print(w)
		w=w+1


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
'''