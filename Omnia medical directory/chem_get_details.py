
from selenium import webdriver
import time
import xlsxwriter
import xlrd

# Open a workbook 
workbook = xlrd.open_workbook('demo.xlsx')  #collect all links from this file
worksheet = workbook.sheet_by_name('Sheet1')

# Load a specific sheet by index 
worksheet = workbook.sheet_by_index(0)

# Retrieve the value from cell at indices (0,0) 
p=worksheet.cell(0, 0).value

url='http://www.omniagmd.com/exhibitordirectory/arab-health'
driver =webdriver.Firefox()

workbook1 = xlsxwriter.Workbook('Main.xlsx')    
worksheet1 = workbook1.add_worksheet()

for i in range(0,3500):    #3500 is number of rows in demo4 file
    p=worksheet.cell(i, 0).value
    driver.get(p)

    while(True):
        try:
            title=driver.find_element_by_xpath("//div[@class='content']//div[@role='article']//div[@class='section-two']//h1")
            title=title.text
        except:
            title="None"
       	worksheet1.write(i,0,title)

        try:
            street=driver.find_element_by_xpath("//div[@class='content']//div[@role='article']//div[@class='section-two']//div[@class='company-address']//div[@class='street-block']")
            street=street.text		
        except:
            street="None"
        worksheet1.write(i,1,street)

        try:
            locality=driver.find_element_by_xpath("//div[@class='content']//div[@role='article']//div[@class='section-two']//div[@class='company-address']//span[@class='locality']")
            locality=locality.text
        except:
            locality="None"
        if(locality=="None"):
            try:
                locality=driver.find_element_by_xpath("//div[@class='content']//div[@role='article']//div[@class='section-two']//div[@class='company-address']//div[@class='locality']")
                locality=locality.text
            except:
                locality="None"
        worksheet1.write(i,2,locality)
		
        try:
            state=driver.find_element_by_xpath("//div[@class='content']//div[@role='article']//div[@class='section-two']//div[@class='company-address']//span[@class='state']")
            state=state.text		
        except:
            state="None"
		
        if state=="None":
            try:
                state=driver.find_element_by_xpath("//div[@class='content']//div[@role='article']//div[@class='section-two']//div[@class='company-address']//div[@class='state']")
                state=state.text		
            except:
                state="None"
       	worksheet1.write(i,3,state)


				
        try:
            postal=driver.find_element_by_xpath("//div[@class='content']//div[@role='article']//div[@class='section-two']//div[@class='company-address']//span[@class='postal-code']")
            postal=postal.text		
        except:
            postal="None"	
		
        if postal=="None":
            try:
                postal=driver.find_element_by_xpath("//div[@class='content']//div[@role='article']//div[@class='section-two']//div[@class='company-address']//div[@class='postal-code']")
                postal=postal.text		
            except:
                postal="None"	
       	worksheet1.write(i,4,postal)
		
		
        try:
            country=driver.find_element_by_xpath("//div[@class='content']//div[@role='article']//div[@class='section-two']//div[@class='company-address']//span[@class='country']")
            country=country.text		
        except:
            country="None"	
		
        if country=="None":
            try:
                country=driver.find_element_by_xpath("//div[@class='content']//div[@role='article']//div[@class='section-two']//div[@class='company-address']//div[@class='country']")
                country=country.text		
            except:
                country="None"
       	worksheet1.write(i,5,country)
				
				
        mobile="None"
        elm=driver.find_element_by_xpath("//div[@class='content']//div[@role='article']//div[@class='section-two']")	
        elm=elm.text
        flag=0
        for h in elm.split('\n'):
            if flag==1:
               mobile=h
               break
            if h==country:
               flag=1

       	worksheet1.write(i,6,mobile)
			   
		
        try:
            website=driver.find_element_by_xpath("//div[@class='content']//div[@role='article']//div[@class='section-two']//div[@class='field field-name-field-company-website field-type-link-field field-label-hidden']//div[@class='field-items']//div[@class='field-item even']//a")
            #website=a.get_attribute('href')
            website=website.text		
        except:
            website="None"	
		
       
       	worksheet1.write(i,7,website)

		
        try:
            des=driver.find_element_by_xpath("//div[@class='content']//div[@role='article']//div[@class='section-two']//p")
            des=des.text		
        except:
            des="None"	
		
        if des=="None":
            try:
                des=driver.find_element_by_xpath("//div[@class='content']//div[@role='article']//span[@class='section-two']//p")
                des=des.text		
            except:
                des="None"
       	worksheet1.write(i,8,des)
				
        break	
					
'''   
    print(title)
    print(street)
    print(locality)
    print(state)
    print(postal)		
    print(country)
    print(mobile)
    print(website)	
    print(des)
    print("\n\n")

'''