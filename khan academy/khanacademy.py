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





courses_link="https://www.khanacademy.org"




'''
html=requests.get(courses_link)

courses=BeautifulSoup(html.text,"lxml")

workbook = xlsxwriter.Workbook('khanacademy_links.xlsx')
worksheet = workbook.add_worksheet()


links=courses.find("ul",{"class":"domains_o3z00m-o_O-domainsFiveColumns_1xgyot8"}).findAll("ul",{"class":"subjectsList_7l3p0"})
#print(links)
print(len(links))

link=None
p=1
for row in links:
	ret=row.findAll("li")
	for i in ret:
		link=i.find("a")['href']
		worksheet.write_url(p,0,courses_link+link)
		link=None
		
		name=i.find("a").find("span").string
		worksheet.write_url(p,1,name)
		print(p)
		p=p+1
print(p)
'''


# Open a workbook 
workbook1 = xlrd.open_workbook('khanacademy_links.xlsx')  #collect all links from this file
worksheet1 = workbook1.sheet_by_name('Sheet1')



workbook = xlsxwriter.Workbook('khanacademy_all_data.xlsx')
worksheet = workbook.add_worksheet()



p=1
for row in range(1,51):#51
	subject_url=worksheet1.cell(row,0).value
	print(subject_url)
	
	subject_name=worksheet1.cell(row,1).value
	print(subject_name)
	
	category=worksheet1.cell(row,2).value
	print(category)
	
	#subject_url="https://www.khanacademy.org/math/algebra2"
	html=requests.get(subject_url)
	courses=BeautifulSoup(html.text,"lxml")
	
	
	#while True:
	try:
		course=courses.find("div",{"class":"moduleList_13hv8io"}).findAll("div",{"class":"content_1gdgprv"})
	except:
		print("Exception here")
		worksheet.write(p,2,subject_url)
		p=p+1
		continue
			
	#print(course)
	for ret in course:
	
		worksheet.write(p,0,category)
		worksheet.write(p,1,subject_name)
		worksheet.write_url(p,2,subject_url)
	
		course_url=ret.find("a")['href']
		
		try:
			courses_name=None
			try:
				courses_name=ret.find("div",{"class":"info_rv4vjm"}).find("h2").string
				print(courses_name)
			except:
				courses_name=ret.find("div",{"class":"info_rv4vjm"}).find("h3").string
				print(courses_name)
		except:
			pass
		course_desc=ret.find("div",{"class":"description_svya6c"}).string
		#print(course_desc)
		
		
		worksheet.write(p,3,courses_name)
		worksheet.write_url(p,4,courses_link+course_url)
		worksheet.write(p,5,course_desc)

		module_len=None
		
		
		#while True:

		try:
			module_len=ret.find("div",{"class":"info_rv4vjm"}).find("p",{"class":"progressNumbers_n8xyv0"})#.string
			#print(module_len)
			module_len=str(module_len).split("of")
			#print(module_len)	
			module_len=module_len[1]
			module_len=str(module_len).split("complete")
			module_len=module_len[0]
			
			module_len=module_len.replace("<!-- /react-text -->","")
			module_len=str(module_len).split("-->")
			module_len=module_len[1]
			module_len=str(module_len).split("<")
			module_len=module_len[0]
			print(module_len)
			
		except:
			print("Exception in module len")
			pass
		
		module=""
		
		data=ret.findAll("div",{"class":"link_ddjp4k"})#.find("ul",{"class":"links_1tgipy2-o_O-links2columns_t4uzd8"}).findAll("div",{"class":"link_ddjp4k"})
		#print(data)
		for k in data:
			#f=k.find("a").string
			#print(f)
			try:
				module=module+str(k.find("a").string)+", "
			except:
				pass
		#print(module)
		worksheet.write(p,6,str(module_len))
		worksheet.write(p,7,module)
		
		p=p+1
		
	



workbook.close()



