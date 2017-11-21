from bs4 import BeautifulSoup
import requests
import urllib.request as ur
import urllib
import re,os,time
from urllib.request import urlopen
import xlsxwriter,xlrd


url="http://www.open.edu/openlearn/free-courses/full-catalogue"

course_link="http://www.open.edu"


workbook = xlsxwriter.Workbook('openlearn_links1.xlsx')
worksheet = workbook.add_worksheet()


html=requests.get(url)
course=BeautifulSoup(html.text,"lxml")

subject=course.find("div",{"class":"view-content"}).findAll("div",{"class":"dropdown-box"})
print(len(subject))
k=1
for each in subject:
	main=each.find("tbody").findAll("tr")
	for i in main:
		link=i.find("a")['href']
		link=course_link+link+"?active-tab=description-tab"
		#print(link)
		worksheet.write_url(k,0,link)
		
		hrs=i.find("td",{"class":"views-field views-field-field-duration views-align-center field_duration"}).string
		worksheet.write(k,1,hrs.strip())
		
		level=i.find("td",{"class":"views-field views-field-field-educational-level views-align-left field_educational_level"}).string
		worksheet.write(k,2,level.strip())
		
		k+=1
		
print(k)

workbook.close()