Omnia is a global medical directory where more than 5000 companies data is stored. when you look at the source code you will come to know it's difficult to get all data directly from website using any tool.
So on the request of one of my client i did some scripting and collect all data in one file.

you need any python ide to run this script. ex. Anaconda, python3 idle
install Selenium using following command.
pip install selenium

Now when you open website you will understand there are many pages in website and at each page there are many companies links.
So we will run two scripts to gather all data.

first run chem_get_links.py file using following command 
python chem_get_links.py
or
python3 chem_get_links.py

After some time one file will create name as demo.xlsx which have all links stored.

now run other file named as chem_get_details.py 
python chem_get_details.py 
or
python3 chem_get_details.py 

It will take lots of time to gather all the data depends on your internet speed and cpu speed.
