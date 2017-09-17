from selenium import webdriver
import time,re
import xlsxwriter
from selenium.webdriver.common.keys import Keys


driver =webdriver.Firefox()
driver.get('https://www.youtube.com/user/tseries/videos')	#paste any channel link here inside double qoutes " "

flag=0
while(True and  flag<=10):  #To grab all links change this line to  while(True):
    driver.execute_script("window.scrollTo(0,Math.max(document.documentElement.scrollHeight," + "document.body.scrollHeight,document.documentElement.clientHeight));")
    flag +=1
    time.sleep(5)

elm=driver.find_elements_by_xpath("//ytd-grid-video-renderer[@class='style-scope ytd-grid-renderer']//div[@id='dismissable']//div[@id='details']//div[@id='meta']//h3[@class='style-scope ytd-grid-video-renderer']//a[@href]")

title=[]
link=[]
for i in elm:
    title.append(i.text)
    link.append(i.get_attribute("href"))
	
'''
print("\n\n\n")

for i in range(0,20):	#remove comment if you want to print upto 20
    print(title[i])
    print(link[i])
'''	

workbook = xlsxwriter.Workbook('T_series.xlsx')  #change file name if exist already
worksheet = workbook.add_worksheet()

worksheet.write(0,0,"Title")
worksheet.write(0,1,"Video Link")



p=2
for i in title:
    worksheet.write(p,0,i)
    p+=1

p=2
for i in link:
    worksheet.write(p,1,i)
    p+=1

workbook.close()
driver.close()
