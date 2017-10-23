import requests
import json
import csv,xlsxwriter,urllib
from bs4 import BeautifulSoup
import codecs

base_url = 'https://www.udemy.com'
mid_url = '/api-2.0/channels/'
change_url = '/courses?is_angular_app=true&is_topic_filters_enabled=true&p=1'


workbook = xlsxwriter.Workbook('udemy_data1111.xlsx')
worksheet = workbook.add_worksheet()
w=0
worksheet.write(w,0,"Image Link")				
worksheet.write(w,1,"Corse Url")
worksheet.write(w,2,"Title")
worksheet.write(w,3,"Description")
worksheet.write(w,4,"Rating")
worksheet.write(w,5,"Students Enrolled")
worksheet.write(w,6,"Last Updated")
worksheet.write(w,7,"Language")
worksheet.write(w,8,"Caption Language")
worksheet.write(w,9,"Todays Price")
worksheet.write(w,10,"Normal Price")
worksheet.write(w,11,"Instructor Name")
worksheet.write(w,12,"Instructor Job")
worksheet.write(w,13,"Course Id")

ee=0
w=2
code = 1624
url = base_url + mid_url + str(code) + change_url
list_courses = []
try:
	while code <= 1652: #You can extend this upto 3028
		print("*****************code**************************")
		print(code)
		try:
			url = base_url + mid_url + str(code) + change_url
			#print(url)
		except:
			continue
		
		while 1 :
			try:
				r = requests.get(url)
				e = json.loads(r.text)
				if str(e) == str({"detail": "Resource not found."}) or str(e)=='' or e==None or str(e)==str({"detail": "Internal server error."}):
					break
				if e['count']==0:
					break
			except Exception as e:
				print(e)
				if str(e)== str("Expecting value: line 1 column 1 (char 0)"):
					break
				continue
			try:
				n = len(e['results'])
				print(n)
				for i in range (0,n) :
					dic = {}
					cat_id = e['results'][i]['id']
					cat_title = e['results'][i]['title']
					cat_url = e['results'][i]['url']
					cat_image_link=e['results'][i]['image_480x270']
					
					try :
						cat_net_price = e['results'][i]['discount']['list_price']['amount']
					except :
						cat_net_price = 0
					
					try :   
						cat_price = e['results'][i]['discount']['price']['amount']
						
					except :
						cat_price = 0
						
					cat_subs = e['results'][i]['num_subscribers']
					cat_rating = e['results'][i]['avg_rating_recent']
					cat_caption = e['results'][i]['caption_languages']
					cat_last_updated = e['results'][i]['published_time']
					cat_lang = e['results'][i]['locale']['english_title']
					cat_inst_name = []
					cat_inst_job = []
					
					number = len(e['results'][i]['visible_instructors'])
					
					for k in range (0,number) :
						cat_inst_name.append(e['results'][i]['visible_instructors'][k]['display_name'])
						cat_inst_job.append(e['results'][i]['visible_instructors'][k]['job_title'])
						
					cat_descr = e['results'][i]['headline']
					
					all_image=cat_image_link
					alt=all_image.split("/")
					alt=alt[-1]
					data = urllib.request.urlopen(all_image).read()
					file = open("Images/"+str(alt), "wb")
					file.write(data)
					file.close()
					worksheet.write_url(w,0,r"Images/"+str(alt))
					
									
					worksheet.write_url(w,1,base_url + cat_url)
					worksheet.write(w,2,str(cat_title))
					worksheet.write(w,3,str(cat_descr))
					worksheet.write(w,4,str(cat_rating))
					worksheet.write(w,5,str(cat_subs))
					worksheet.write(w,6,str(cat_last_updated))
					worksheet.write(w,7,str(cat_lang))
					worksheet.write(w,8,str(' '.join(cat_caption)))
					worksheet.write(w,9,str(cat_price))
					worksheet.write(w,10,str(cat_net_price))
					worksheet.write(w,11,str(' '.join(cat_inst_name)))
					worksheet.write(w,12,str(' '.join(cat_inst_job)))
					worksheet.write(w,13,cat_id)
					
					w+=1
					print(w)

				if e['pagination']['current_page'] == e['pagination']['total_page'] :
					break		
				url = base_url + e['pagination']['next']['url']
			except:
				if e['pagination']['current_page'] == e['pagination']['total_page'] :
					break		
				url = base_url + e['pagination']['next']['url']	
				print("exception")
				print(ee)
				ee+=1
				

		code += 2
		
except Exception as e:
	print(e)
	print(cat_id)
	
finally:
	workbook.close()
	
workbook.close()
