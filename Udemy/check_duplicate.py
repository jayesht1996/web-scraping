import time
import xlsxwriter
import xlrd

# Open a workbook 
workbook = xlrd.open_workbook('final_udemy.xlsx')
worksheet1 = workbook.sheet_by_name('Sheet1')

#24926+19050+144
workbook2 = xlsxwriter.Workbook('Final_collected_udemy_data.xlsx')
worksheet2 = workbook2.add_worksheet()
try:
	p=1
	for i in range(0,130317): #Divide this in small parts
		link=worksheet1.cell(i, 1).value
		flag=1
		for j in range(1,i):
			link1=worksheet1.cell(j, 1).value
			if(link == link1):
				flag=0
				break
		if flag==1:
			title=worksheet1.cell(i, 0).value
			ins=worksheet1.cell(i, 1).value
			lin=worksheet1.cell(i, 2).value
			dur=worksheet1.cell(i, 3).value
			lev=worksheet1.cell(i, 4).value
			views=worksheet1.cell(i, 5).value
			rel=worksheet1.cell(i, 6).value
			desc=worksheet1.cell(i, 7).value
			image=worksheet1.cell(i, 8).value
			a9=worksheet1.cell(i, 9).value
			a10=worksheet1.cell(i, 10).value
			a11=worksheet1.cell(i, 11).value
			a12=worksheet1.cell(i, 12).value
			a13=worksheet1.cell(i, 13).value
			a14=worksheet1.cell(i, 14).value


			worksheet2.write_url(p,0,title)
			worksheet2.write_url(p,1,ins)
			worksheet2.write(p,2,lin)
			worksheet2.write(p,3,dur)
			worksheet2.write(p,4,lev)
			worksheet2.write(p,5,views)
			worksheet2.write(p,6,rel)
			worksheet2.write(p,7,desc)
			worksheet2.write(p,8,image)
			worksheet2.write(p,9,a9)
			worksheet2.write(p,10,a10)
			worksheet2.write(p,11,a11)
			worksheet2.write(p,12,a12)
			worksheet2.write(p,13,a13)
			worksheet2.write(p,14,a14)
			p=p+1
			print(p)
except Exception as e:
	print(e)
finally:
	workbook2.close()
workbook2.close()
