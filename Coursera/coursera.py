
from bs4 import BeautifulSoup
import requests,re
import csv,xlsxwriter
import os,urllib

api_url = "https://api.coursera.org/api/courses.v1?start=0&limit=2890&includes=instructorIds,partnerIds,specializations,s12nlds,v1Details,v2Details&fields=instructorIds,partnerIds,specializations,s12nlds,description"
data = requests.get(api_url).json()


workbook = xlsxwriter.Workbook('coursera_next_2.xlsx')
worksheet = workbook.add_worksheet()

url='https://www.coursera.org/learn/'
slug=[]
for each in data['elements']:
    slug.append(each['slug'])
print(len(slug))

p=1
for row in range(0,len(slug)):
	try:
		link=url+slug[row]
		#link="https://www.coursera.org/learn/climate-science"
		worksheet.write_url(p,0,link)
		topic_courses=requests.get(link)
		course=BeautifulSoup(topic_courses.text,'lxml')
	except Exception as e:
		print(e)
		continue
		
	try:
		subject=course.find("div",{"class":"rc-BannerBreadcrumbs caption-text"})
		sub=subject.findAll("span")
		
		#print(len(sub))
		
		try:
			subj=sub[1].find("a").string
			worksheet.write(p,1,subj)
		except:
			worksheet.write(p,1,"None")
			
		try:
			topic=sub[2].find("a").string
			worksheet.write(p,2,topic)
		except:
			worksheet.write(p,2,"None")
			
	except:
		pass
		
	try:
		title=course.find("div",{"class":"bt3-col-sm-9 bt3-col-sm-offset-3 header-container"}).find("h1").string
		worksheet.write(p,3,title)
	except:
		worksheet.write(p,3,"None")
		
	try:
		about=course.find("div",{"class":"content-inner"}).find("p",{"class":"body-1-text course-description"})#.string
		#print(about)
		ab=str(about).split("-->")
		#print(ab[1])
		worksheet.write(p,4,ab[1])
	except:
		worksheet.write(p,4,"None")
		
	
	try:
		about=course.find("div",{"class":"rc-Overview"}).find("div",{"class":"target-audience-section"}).find("p",{"class":"body-1-text course-description"})#.string
		#print(about)
		ab=str(about).split("-->")
		#print(ab[1])
		worksheet.write(p,5,ab[1])
	except:
		worksheet.write(p,5,"None")
		
	try:
		create=course.find("div",{"class":"rc-CreatorInfo"}).find("div",{"class":"headline-1-text creator-names"}).findAll("span")
		worksheet.write(p,7,create[1].string)
		#print(create[1].string)
	except:
		worksheet.write(p,7,"None")
	
	try:
		create_logo=course.find("div",{"class":"rc-CreatorInfo"}).find("div",{"class":"creator-logos horizontal-box"}).find("img")['src']
		create_logo=create_logo.replace("https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/","")
		
		print(create_logo)
		alt=create_logo.split("/")
		alt=alt[-1]
		alt=alt.split("?")
		alt=alt[0]
		data = urllib.request.urlopen(create_logo).read()
		file = open("Provider/"+str(alt), "wb")
		file.write(data)
		print(alt)
		worksheet.write_url(p,6,r"Provider/"+str(alt))
		#worksheet.write(p,6,create_logo)
		#print(create_logo)
	except:
		worksheet.write(p,6,"None")
		
	try:
		create_dsc=course.find("div",{"class":"partner color-primary-text"}).find("div",{"class":"body-1-text"}).string
		worksheet.write(p,8,create_dsc)
		#print(create[1].string)
	except:
		worksheet.write(p,8,"None")
	
		
		
		
		
	try:
		flag1=False
		flag2=False
		flag3=False
		flag4=False
		flag5=False
		flag6=False
		flag7=False
		flag8=False
		table=course.find("table",{"class":"basic-info-table bt3-table bt3-table-striped bt3-table-bordered bt3-table-responsive"}).find("tbody").findAll("tr")
		for i in table:
			che=i.find("span",{"class":"td-title"}).string
			#print(che)
			if che=="Level":
				level=i.find("td",{"class":"td-data"}).string
				worksheet.write(p,9,level)
				flag1=True
			elif che=="Commitment":
				com=i.find("td",{"class":"td-data"}).string
				worksheet.write(p,10,com)
				flag2=True
			elif che=="Language":
				lang=i.find("td",{"class":"td-data"}).find("div",{"class":"rc-Language"})
				#print(lang)
				lan=str(lang).split("-->")
				main=lan[1].split("<")
				#print(main[0])
				sub=""
				try:
					ll=i.find("td",{"class":"td-data"}).find("div",{"class":"rc-Language"}).find("span")
					ss=str(ll).split("-->")
					te=ss[1].split("<!--")
					sub="  Subtitles : "+te[0]
					print(sub)
				except:
					pass
				worksheet.write(p,11,main[0]+sub)
				flag3=True
			elif che=="How To Pass":
				pas=i.find("td",{"class":"td-data"}).string
				worksheet.write(p,12,pas)
				flag4=True
			#elif che=="User Ratings":
			#	reti=i.find("td",{"class":"td-data"}).find("div",{"class":"ratings-text bt3-hidden-xs"}).string
			#	worksheet.write(p,13,reti)
			#	flag6=True
			elif che=="Basic Info":
				spec=i.find("td",{"class":"td-data"}).find("div",{"class":"rc-CourseS12nInfo"}).find("a").string
				worksheet.write(p,13,spec) 
				flag7=True
	except:
		pass
	if flag1==False:
		worksheet.write(p,9,"None")
	if flag2==False:
		worksheet.write(p,10,"None")
	if flag3==False:
		worksheet.write(p,11,"None")
	if flag4==False:
		worksheet.write(p,12,"None")
	if flag7==False:
		worksheet.write(p,13,"No")
	
				
	try:
		syllabus=course.find("div",{"class":"rc-WeekView"}).findAll("div",{"class":"week"})
		week=""
		for i in syllabus:
			try:
				name=i.find("div",{"class":"week-heading body-2-text"}).string
				week+=name+" : "
			except:
				pass
			try:
				module=i.find("div",{"class":"module-name headline-2-text"}).string
				week+=module
			except:
				pass
			try:
				txt=i.find("div",{"class":"module-desc body-1-text"}).string
				#print(txt)
				week+=txt+"   "
			except:
				pass
			#print(week)
			
		worksheet.write(p,14,week)	
	except:
		worksheet.write(p,14,"None")
	
	try:
		rett=course.find("div",{"class":"rc-RatingsHeader horizontal-box align-items-absolute-center"}).find("div",{"class":"ratings-text headline-2-text"}).find("span")
		rett=str(rett).split("-->")
		rett=rett[1].split("<!--")
		
		#print(rett[0])
		
		worksheet.write(p,15,rett[0])	
	except:
		worksheet.write(p,15,"None")
		
		
	try:
		rated=course.find("div",{"class":"rc-RatingsHeader horizontal-box align-items-absolute-center"}).find("div",{"class":"ratings-text headline-2-text"}).find("span").find("span").string
		#print(rated)
		
		worksheet.write(p,16,rated)	
	except:
		worksheet.write(p,16,"None")
		
		
	try:
		images=course.find("div",{"class":"rc-PhoenixCdpBanner"}).find("div",{"class":"body-container"})['style']
		#print(images)
		images=images.replace("background-image:url(https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/","")
		
		alt=images.split("/")
		alt=alt[-1]
		alt=alt.split("?")
		alt=alt[0]
		data = urllib.request.urlopen(images).read()
		file = open("Cover/"+str(alt), "wb")
		file.write(data)

		worksheet.write_url(p,17,r"Cover/"+str(alt))
		#worksheet.write(p,17,images)	
	except:
		worksheet.write(p,17,"None")
		
		
	w=19
	try:
		ins=course.find("ul",{"class":"instructors-section nostyle"}).findAll("li")
		#print(len(ins))
		for i in range(len(ins)):
			try:
				pic=ins[i].find("div",{"class":"instructor-photo bt3-col-xs-4 bt3-col-sm-2"}).find("a").find("img")['src']
				#print(pic)
						
				pic=pic.replace("https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/","")
				
				alt=pic.split("/")
				alt=alt[-1]
				alt=alt.split("?")
				alt=alt[0]
				data = urllib.request.urlopen(pic).read()
				file = open("Instructor/"+str(alt), "wb")
				file.write(data)

				worksheet.write_url(p,w,r"Instructor/"+str(alt))
				#worksheet.write_url(p,w,pic)
			except:
				w=w+1
				worksheet.write(p,w,"None")
			try:
				name=ins[i].find("p",{"class":"instructor-name"}).find("span",{"class":"body-1-text"}).find("a").string
				#print(name)
				det=ins[i].find("p",{"class":"instructor-name"}).find("span",{"class":"body-1-text"})
				ab=str(det).split("-->")
				name=name+ab[1]
				#print(name)
				w=w+1
				worksheet.write(p,w,str(name))
				#print(w)
			except KeyboardInterrupt:
				w=w+1
				worksheet.write(p,w,"None")
			try:
				ins_bio=name=ins[i].find("div",{"class":"instructor-info bt3-col-xs-8 bt3-col-sm-10"}).find("div",{"class":"instructor-bio caption-text color-accent-brown"}).string
				#print(ins_bio)
				w=w+1
				worksheet.write(p,w,ins_bio)
			except:
				w=w+1
				worksheet.write(p,w,"None")
			w=w+1
	except:
		pass
		
		
		
	print("line  "+str(p))
	p+=1
workbook.close()