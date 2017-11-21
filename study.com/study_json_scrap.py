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




# Open a workbook 
workbook1 = xlrd.open_workbook('study_all_json.xlsx')  #collect all links from this file
worksheet1 = workbook1.sheet_by_name('Sheet1')


workbook = xlsxwriter.Workbook('study_all_data_1.xlsx')
worksheet = workbook.add_worksheet()

course_link="https://www.study.com"
add=0
r=1

for row in range(1,4131):
	link=worksheet1.cell(row, 0).value
	html=requests.get(link)
	course=BeautifulSoup(html.text,"lxml")

	image=worksheet1.cell(row, 4).value
	alt=image.split("/")
	alt=alt[-1]

	data = urllib.request.urlopen(image).read()
	file = open("Images/"+str(alt), "wb")
	file.write(data)
	file.close()	
	
	worksheet.write_url(r,0,link)
	
	title=worksheet1.cell(row, 1).value
	worksheet.write(r,1,title)
	
	
	worksheet.write_url(r,4,image)
	worksheet.write_url(r,3,r"Images/"+str(alt))
	
	try:
		desc=course.find("div",{"class":"courseSummary"})
		desc=str(desc)
		desc=desc.split("</h3>")
		desc=desc[1]
		desc=desc.split("<div")
		desc=desc[0].replace("\n","")
		desc=desc.strip(" ")
		#print(desc)
		worksheet.write(r,2,desc)
	except:
		worksheet.write(r,2,"None")
		
	
	view=worksheet1.cell(row, 2).value
	worksheet.write(r,5,view)
	
	
	lesson=worksheet1.cell(row, 3).value
	worksheet.write(r,6,lesson)
	
	try:
		label=course.find("div",{"class":"courseOverviewModule"}).find("div",{"class":"courseOverview"}).find("ul").findAll("li")
	except:
		pass
	tt=0
	for item in label:
		#print(item)
		try:
			try:
				i=item.find("b").string
			except:
				#print("Exception")
				continue
			'''
			if tt>4:
				break
			tt+=1
			'''
			if "Course type:" in i:
				try:
					l=str(item)
					l=l.split('</b>')
					l=l[1].split('</li>')
					l=l[0]
					l=l.replace("\n","")
					l=l.replace(" ","")
					l=l.replace("\t","")
					#print(l)
				
					#worksheet.write(k,5,type)
					worksheet.write(r,7,l)
				except:
					worksheet.write(r,7,"None")
			elif "Available Lessons:" in i:
				try:
					l=str(item)
					l=l.split('</b>')
					l=l[1].split('</li>')
					l=l[0]
					l=l.replace("\n","")
					l=l.replace(" ","")
					l=l.replace("\t","")
					#print(l)
					#worksheet.write(r,5,l)
				except:
					pass
					#worksheet.write(r,5,"None")
			elif ("Average Lesson" in i)==True:
				try:
					l=str(item)
					l=l.split('</b>')
					l=l[1].split('</li>')
					l=l[0]
					l=l.replace("\n","")
					l=l.replace(" ","")
					l=l.replace("\t","")
					#print(l)
					worksheet.write(r,8,l)
				except:
					worksheet.write(r,8,"None")
					
			elif("Eligible for" in i)==True:
				try:
					if "Eligible for Credit:" in i:
						worksheet.write(r,9,"Yes")
					else:
						worksheet.write(r,9,"No")
					
				except:
					worksheet.write(r,9,"None")
		except:
			print(ret)
			

	try:
		subject=course.find("div",{"class":"left-content"})
		l=str(subject)
		
		l=l.split("</span>")
		l=l[1].split("<")
		l=l[0]
		l=l.replace("\n","")
		l=l.replace(" ","")
		l=l.replace("\t","")
		#print(l)
		worksheet.write(r,10,l)
	except:
		worksheet.write(r,10,"None")
		
		
		
		
	upvote=worksheet1.cell(row, 6).value
	worksheet.write(r,11,upvote)
		
	downvote=worksheet1.cell(row, 7).value
	worksheet.write(r,12,downvote)
		
	date=worksheet1.cell(row, 8).value
	worksheet.write(r,13,date)
		
	resc=worksheet1.cell(row, 9).value
	worksheet.write(r,14,resc)
		
	res=str(worksheet1.cell(row, 10).value)
	worksheet.write(r,15,res)
	
	exam=worksheet1.cell(row, 11).value
	worksheet.write_url(r,16,exam)
	
		
	print(r)
	r=r+1

workbook.close()