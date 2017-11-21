from bs4 import BeautifulSoup
import requests
import urllib.request as ur
import urllib
import re,os,time
from urllib.request import urlopen
import xlsxwriter,xlrd


url="http://oyc.yale.edu/courses"

course_link="http://oyc.yale.edu"


workbook = xlsxwriter.Workbook('oyc_links2.xlsx')
worksheet = workbook.add_worksheet()


html=requests.get(url)
course=BeautifulSoup(html.text,"lxml")

links=course.find("table",{"class":"views-table cols-5"}).find("tbody").findAll("tr")
print(len(links))


k=0
for i in links:
	link=i.find("td",{"class":"views-field views-field-title active"}).find("a")['href']
	link=course_link+link
	#print(link)
	worksheet.write_url(k,0,link)
	
	depart=i.find("td",{"class":"views-field views-field-title active"}).find("a").string
	worksheet.write(k,1,depart)
	
	
	no=i.find("td",{"class":"views-field views-field-field-course-number"}).find("a").string
	worksheet.write(k,2,no)
	
	title=i.find("td",{"class":"views-field views-field-title-1"}).find("a").string
	worksheet.write(k,3,title)
	
	title_link=i.find("td",{"class":"views-field views-field-title-1"}).find("a")['href']
	worksheet.write_url(k,6,course_link+title_link)
	
	ins=i.find("td",{"class":"views-field views-field-field-professors-last-name"}).string
	worksheet.write(k,4,ins.strip())
	
	
	date=i.find("td",{"class":"views-field views-field-field-semester"}).string
	worksheet.write(k,5,date.strip())
	
	
	k+=1
		
print(k)

workbook.close()