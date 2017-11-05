from bs4 import BeautifulSoup
import requests
import xlwt
import xlrd
import urllib.request as ur
import urllib
import re
from urllib.request import urlopen
import xlsxwriter

workbook = xlsxwriter.Workbook('plural_sight_data4.xlsx')
worksheet = workbook.add_worksheet()


worksheet.write(0,0,'Course Name')
worksheet.write(0,1,'Instructor and Details')
worksheet.write(0,2,'Couse Level')
worksheet.write(0,3,'Ratings')
worksheet.write(0,4,'Total No of People Rated the Course')
worksheet.write(0,5,'Course Updated On')
worksheet.write(0,6,'Duration')
worksheet.write(0,7,'Start Free Trial Now Link')
worksheet.write(0,8,'Course Signup Link')
worksheet.write(0,9,'Image Link')

r=1
print("Please wait,this might take a few minutes")
page = requests.get("https://www.pluralsight.com/catalog")   #open the main catalogue page
soup = BeautifulSoup(page.content, 'html.parser')

val=soup.findAll('a', attrs={'class':'tableview-row'})
print(len(val))

r=1
for a in range(4453,len(val)):
	 try:
		 link=val[a].get('href')              #for getting link to individual course page
		 link="https://www.pluralsight.com/"+ link
		 course_page=requests.get(link)      #for getting data from individual course page
		 course_soup = BeautifulSoup(course_page.content, 'html.parser')
		 print(r)
		 worksheet.write_url(r,0,link) 
		 img=course_soup.find("div",{"id":"course-page-hero"})['style']
		 print(img)
		 worksheet.write_url(r,1,img) 
		 r+=1
	 except KeyboardInterrupt:
		 print("exception")
		 break
	 except Exception as e:
		 print(e)
		 continue
workbook.close()
		 
'''		 
d=soup.findAll('div', attrs={'class':'type-md medium'})
print(len(d))

for a in range(0,len(val)):
	 try:
		 link=val[a].get('href')              #for getting link to individual course page
		 link="https://www.pluralsight.com/"+ link
		 course_page=requests.get(link)      #for getting data from individual course page
		 course_soup = BeautifulSoup(course_page.content, 'html.parser')
		 print(r)
		  #get the course name
		 worksheet.write_url(r,11,link) 
		 course_name = course_soup.find(name='h1')
		 if course_name:
			 worksheet.write(r,0,course_name.get_text())
			
		# get the author name
		 by_tag=course_soup.find(name='h5')
		 if 'By' in by_tag.get_text():
			 author_name=by_tag.get_text()
			 author_name=author_name[3:]
		 #get the author details
		 about_the_author= course_soup.find(name='h6',text="About the author")
		 author_details="Not Found"
		 if about_the_author:
			 author_details = about_the_author.find_next_sibling('p')
		 worksheet.write(r,1,author_name +":"+ author_details.get_text())
		 #get the course level
		 level_tag=course_soup.find(name='div',text="Level")
		 course_level=level_tag.find_next_sibling('div').get_text()
		 worksheet.write(r,2,course_level)
		
		
		 #get the rating in stars and the number of raters
		 rating_div= course_soup.find('div',{'class':'course-info__row--right course-info__row--rating'})
		 num_of_raters=0
		 if rating_div is not None:
			 full_stars_count =float(len(rating_div.find_all(class_="fa fa-star")))
			 half_stars_count=len(rating_div.find_all(class_="fa fa-star-half-o"))
			 num_of_raters=(rating_div.find('span').get_text()).strip("()")
			 if half_stars_count:
				 rating=float(full_stars_count + 0.5)
			 else:
				 rating=full_stars_count
		 else:
			 rating= 0
			
		 worksheet.write(r,3,rating)
		 
		 worksheet.write(r,4,num_of_raters)
		 
		 #get the date the course was last updated
		 tag_updated=course_soup.find(name='div',text="Updated")
		 date_updated = tag_updated.find_next_sibling('div').get_text()
		 worksheet.write(r,5,date_updated)
		 try:
			 image=course_soup.find("div",{"class":"author_image_mask"}).find("img")['src']
			 #print(image)
		 
			 worksheet.write(r,9,image)
		 except:
			 worksheet.write(r,9,"None")
		 
		 try:		
			 alt=image.split("/")
			 alt=alt[-1]
			 data = urllib.request.urlopen(image).read()
			 file = open("Images/"+str(alt), "wb")
			 file.write(data)
			 file.close()	
			 worksheet.write_url(r,10,r"Images/"+str(alt))
		 except:
			 worksheet.write(r,10,"None")
				
		 
		 #get the duration of the course 
		 tag_duration=course_soup.find(name='div',text="Duration")
		 duration = tag_duration.find_next_sibling('div').get_text()
		 worksheet.write(r,6,duration)

		 
		 #get the start free trial now link
		 free_trial_tag= course_soup.find('a',text="Start free trial now")
		 free_trial_link=free_trial_tag.get('href')
		 worksheet.write_url(r,7,free_trial_link)

		 
		 #get the course sign-up link
		 course_signup_tag= course_soup.find('a',text="Start free trial now")
		 course_signup_link=course_signup_tag.get('href')
		 worksheet.write_url(r,8,course_signup_link)

		 
		 course_page.close() # close the page opened by the individual course link
		 r=r+1
		 
		 #remove this if condition if you want to get the entire results
		 #if r>10:
			# break
	 except KeyboardInterrupt:
		 workbook.close()
		 break
	 except Exception as e:
		 print(e)
		 print(r)
		 
workbook.close()
print ("Done writing to the output file: PluralSights_Catalog_Scraped_Output.xls")
print("Please check your current directory for this file")

'''
