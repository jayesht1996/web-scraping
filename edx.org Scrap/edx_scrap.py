from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
import urllib.request


driver = webdriver.Firefox()

#main edX page of all English courses -- this scraper excludes edX courses in other languages
#there are total five different links from where you are scraping data
#To avoid robots of edx i have divided this script in different five parts
#You have to run this script five times by changing its url and csv file name

driver.get('https://www.edx.org/course/?availability=current')
#https://www.edx.org/course/?availability=current
#https://www.edx.org/course/?availability=starting_soon
#https://www.edx.org/course/?availability=upcoming
#https://www.edx.org/course/?availability=Self-Paced
#https://www.edx.org/course/?availability=archived







#open a new blank csv and change the name for different website
csv_file = open('courses_whole_current1.csv', 'w',encoding='utf-8')
#courses_whole_current.csv

writer = csv.writer(csv_file)


writer.writerow(['Course name','Course link','Cover image','Institution','Verified','Start date','Self Paced','Video link','Short description','Course provider image','Enroll now link','About course','Overall rating','All reviews','Instructor name','instructor details','Instructor photo','Course price','length','Effort','Subject','Level','Video transcript','Languages'])

num_classes_str = driver.find_element_by_xpath('//span[@class="js-count result-count"]').text

#convert total course number to an integer
num_classes = int((re.findall(r'\d+', num_classes_str))[0])

#initialize page number = 0
page = 0

###   this while loop scrolls down the main course page until all courses are loaded
#We check num_classes*2 for safe side and to load more and more data
print(num_classes)
while page < (num_classes*2):
    
    #driver does an initial scroll down to bottom of the page
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    #this try command waits until it can see the "loading..." icon. Once it sees the icon, we add 1 to page counter
    #and continue at the top of the while loop to do another scroll
	try:
		WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="loading"]')))
		page += 1
		print(page)

    #when the driver waits 10 seconds and still cannot see the "Loading..." icon, it will raise an exception
    #at this point, we will be at bottom of the page, all courses visible, break out of the loop
	except Exception as e:
		print(e)
		print(page)
		break

#get a list of all course link xpath elements
courses = driver.find_elements_by_xpath('//div[@class="discovery-card-inner-wrapper"]/a[@class="course-link"]')
ban=driver.find_elements_by_class_name("banner")
banner=[]
for b in ban:
    banner.append(b.text)
	
img=[]
pic=[]
pics=driver.find_elements_by_class_name("img-wrapper")
for i in pics:
    image = i.find_element_by_tag_name("img")
    img.append(image.get_attribute("src"))

pic=img

#initialize empty list
course_links = []

#for each course link xpath, grab the link itself (the href element) and append it to the course_link list
for course in courses:
    course_links.append(course.get_attribute('href'))
print(len(courses))
#get title of course
def get_title():
    try:
        title = driver.find_element_by_xpath('.//*[@id="course-info-page"]//h1[@id="course-intro-heading"]').text
    except:
        title = 'Missing'
    finally:
        return title

#get short description of course
def get_short_description():
    try:
        short_description = driver.find_element_by_xpath('.//*[@id="course-info-page"]//p[@class="course-intro-lead-in"]').text
    except:
        short_description = 'Missing'
    finally:
        return short_description

#get length of course (typically number of weeks, or total number of hours)
def get_length():
    try:
        length = driver.find_element_by_xpath('.//*[@id="course-summary-area"]//li[@data-field="length"]/span[2]').text
    except:
        length = 'Missing'   
    finally:
        return length

#get the effort of course (typically hours per week, or total course hours)
def get_effort():
    try:
        effort = driver.find_element_by_xpath('.//*[@id="course-summary-area"]//li[@data-field="effort"]//span[@class="block-list__desc"]').text
    except:
        effort = 'Missing'
    finally:
        return effort

def get_languages():
    try:
        lang = driver.find_element_by_xpath('.//*[@id="course-summary-area"]//li[@data-field="language"]//span[@class="block-list__desc"]').text
    except:
        lang = 'Missing'
    finally:
        return lang

#get the price of course. The first "try" only works for free courses. This grabs the text "FREE" by xpath
#to get the price of not-free courses, the "except, try" gets the unique "tag" icon, then jumps to the parent 
#span class, then to a sibling span class to get the price amount. Unfortunately, the price amount doesn't 
#have a unique identifier.

def get_price():
    try:
        price = driver.find_element_by_xpath('.//*[@id="course-summary-area"]//li[@data-field="price"]//span[@class="block-list__desc"]/span[@class="uppercase"]').text
    except:
        try:                               
            price = driver.find_element_by_xpath('.//*[@id="course-summary-area"]//span[@class="fa fa-tag fa-lg"]]/../parent::span/following-sibling::span').text()
        except:
            price = "Missing"
    finally:
        return price
    
#gets the institution
def get_institution():
    try:
        institution = driver.find_element_by_xpath('.//*[@id="course-summary-area"]//li[@data-field="school"]/span[2]/a').text
    except:
        institution = 'Missing'
    finally:
        return institution

#gets the subject
def get_subject():
    try:
        subject = driver.find_element_by_xpath('.//*[@id="course-summary-area"]//li[@data-field="subject"]/span[2]/a').text
    except:
        subject = 'Missing'
    finally:
        return subject

#gets the level (introductory, intermediate, advanced)
def get_level():
    try:
        level = driver.find_element_by_xpath('.//*[@id="course-summary-area"]//li[@data-field="level"]//span[@class="block-list__desc"]').text
    except:
        level = 'Missing'
    finally:
        return level

#gets the prerequisites, if any
def get_prerequisites():
    try:
        prerequisites = driver.find_element_by_xpath('.//*[@id="course-summary-area"]/div[2]/p').text
    except:
        try:
            prerequisites = driver.find_element_by_xpath('.//*[@id="course-summary-area"]/div[2]/ul/li[1]')
        except:
            prerequisites = 'Missing'
    finally:
        return prerequisites
		
def get_about():
	try:
		about = driver.find_element_by_xpath('.//*[@class="content-grouping"]//div[@class="course-description wysiwyg-content"]//div[@class="see-more-content"]').text
		#p=about.split("\n")
		#	about=p[0]
		#print(about)
	except:
		about = 'Missing'
	finally:
		return about

def get_reviews():
    try:
        rev = driver.find_element_by_xpath('.//*[@class="content-grouping"]//span[@class="ct-widget-stars"]/a').text
    except:
        rev = 'Missing'
    finally:
        return rev

		
	

def get_ratings():
    try:
        rat = driver.find_element_by_xpath('.//*[@class="content-grouping"]//span[@class="ct-widget-stars"]//span[@class="ct-widget-stars__rating-stat"]').text
    except:
        rat = 'Missing'
    finally:
        return rat

def enroll():
	try:
		rat = driver.find_element_by_xpath('.//*[@class="media-block"]//div[@class="enroll-outro"]//a[@class="btn btn-cta txt-center js-enroll-btn "]')
		rat=rat.get_attribute('href')
	except:
		rat = 'Missing'
	finally:
		return rat


def self_paced():
	try:
		rat = driver.find_element_by_xpath('.//*[@class="course-side-area"]//div[@class="course-start"]').text
		if "Self-Paced" in rat:
			rat="Yes"
		else:
			rat="No"
	except:
		rat = 'Missing'
	finally:
		return rat
		
def start_date():
	try:
		rat = driver.find_element_by_xpath('.//*[@class="course-side-area"]//div[@class="course-start"]/span').text
	except:
		try:
			rat = driver.find_element_by_xpath('.//*[@class="course-side-area"]//div[@class="course-start"]/div').text
		except:
			rat = 'Missing'
	finally:
		return rat


def video():
	try:
		rat = driver.find_element_by_xpath('.//*[@class="course-header course-header-no-promo"]//div[@class="course-detail-video"]/img')
		rat=rat.get_attribute('src')
		#print (rat)
	except:
		rat = 'Missing'
	finally:
		return rat


def ins_name():
    try:
        rat = driver.find_element_by_xpath('.//*[@class="clear-list list-instructors clearfix"]//li[@class="list-instructor__item"]//a[@target="_blank"]//p[@class="instructor-name"]').text
    except:
        rat = 'Missing'
    finally:
        return rat
		

def ins_info():
    try:
        rat = driver.find_element_by_xpath('.//*[@class="clear-list list-instructors clearfix"]//li[@class="list-instructor__item"]//p[@class="instructor-position"]').text
    except:
        rat = 'Missing'
    finally:
        return rat
		
def get_transcripts():
	try:
		ret = driver.find_element_by_xpath('.//*[@id="course-summary-area"]//li[@data-field="video-transcript"]//span[@class="block-list__desc"]').text
		print(ret)
	except:
		ret = 'Missing'
	finally:
		return ret

def get_logo():
	try:
		p="1"
		rat = driver.find_element_by_xpath('.//*[@class="fixed-width-sidebar"]//a[@class="course-org-link"]/img')
		rat=rat.get_attribute('src')
		
		'''
		p=rat.split("/")
		p=p[-1]
		print (rat)
		print (p)
		urllib.request.urlretrieve(rat, p)
		'''

	
	except:
		rat = 'Missing'
		#p=rat
	finally:
		return rat

def get_image(k):
	try:
		p="1"
		rat = pic[k]
		'''
		#rat=rat.get_attribute('src')
		p=rat.split("/")
		p=p[-1]
		data = urllib.request.urlopen(rat).read()
		file = open("Images/"+p, "wb")
		file.write(data)
		file.close()

		print (rat)
		print (p)
		#urllib.request.urlretrieve(rat, "Images/"+p)
		'''
	except:
		rat = 'Missing'
		#p=rat
		
	finally:
		return rat

		
def get_banner(k):
	try:
		banner=ban[k]
		banner=banner.text
		print(banner)
		if banner=="Verified" or	 banner=="VERIFIED":
		    flag="Yes"
		else:
			flag="No"
		
	except:
		#print("ooo")
		flag=None
	finally:
		return flag
		
		
		
		
		
		
		
###  this for loop:
###     1) iterates through each of the course links
###     2) creates a new empty dictionary
###     3) directs the driver to the link
###     4) calls each of the scraping functions above and saves the return values in the dictionary
###     5) writes the dictionary values out to the csv
k=0
for course_link in course_links:
	course_dict = {}
	driver = webdriver.Firefox()
	driver.get(course_link)
	print(k)
	   
	course_dict['name'] = get_title()
	course_dict['link'] = course_link
	course_dict['cover'] = get_image(k)
	course_dict['institution'] = get_institution()
	course_dict['verified'] = get_banner(k)
	course_dict['date'] = start_date()
	course_dict['self_paced'] = self_paced()
	course_dict['video'] = video()

	course_dict['short_description'] = get_short_description()
	course_dict['logo'] = get_logo()
	course_dict['enroll '] = enroll()
	course_dict['about'] = get_about()
	course_dict['ratings'] = get_ratings()
	course_dict['reviews'] = get_reviews()
	course_dict['ins_name'] = ins_name()
	course_dict['ins_info'] = ins_info()
	course_dict['ins_photo'] = "None"
	course_dict['price'] = get_price()

	course_dict['length'] = get_length()
	course_dict['effort'] = get_effort()
	course_dict['subject'] = get_subject()

	course_dict['level'] = get_level()

	course_dict['video_transcript'] = get_transcripts()
	course_dict['language'] = get_languages()
	writer.writerow(course_dict.values())
	driver.close()
	k+=1

#close the csv once all course info is scraped
csv_file.close()