from selenium import webdriver
import time
import xlsxwriter

url='http://www.omniagmd.com/exhibitordirectory/arab-health'

driver =webdriver.Firefox()
driver.get(url)	


workbook = xlsxwriter.Workbook('demo.xlsx')
worksheet = workbook.add_worksheet()
list=[]
c=1

while(c<=288):
    for a in driver.find_elements_by_xpath("//div[@class='directory-exhibitor']//div[@role='article']//div[@class='section-two']//h3/a"):
        list.append(a.get_attribute('href'))
        #l=a.get_attribute('href')
        #worksheet.write(p,0,l)
    if(c!=288):	
        driver.find_element_by_xpath("//li[@class='pager-next']").click()
	
    c+=1
p=0
for i in list:
    worksheet.write(p,0,i)
    p+=1

workbook.close()
driver.close()