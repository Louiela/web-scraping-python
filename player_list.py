import sys
import requests
import operator
import json
import urllib
import os, errno
from bs4 import BeautifulSoup

def check_directory_exist(path_to_file):
    if not os.path.exists(os.path.dirname(path_to_file)):
        try:
            os.makedirs(os.path.dirname(path_to_file))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def check_file_exist(file_to_check):
    return os.path.isfile(file_to_check)


def download_file_to_directory(url_file_to_download , local_file_to_download):
    f = open(local_file_to_download,'wb')
    f.write(requests.get(url_file_to_download).content)
    f.close()



#define variable
domain = 'http://xn--42c2bi7an0cb9p.com/'
# image directory -- C:\Users\lou.dulguime\Documents\Projects\python\bkk\images\player-img
local_flag_image_directory = '/Users/lou.dulguime/Documents/Projects/python/bkk/images/player-img/'


url_to_scrape = 'http://xn--42c2bi7an0cb9p.com/thaiformer.php'
r = requests.get(url_to_scrape) # get html source
soup = BeautifulSoup(r.text,'html.parser') # parsing data to BeautifulSoup
main_table = soup.select_one("table:nth-of-type(1)") # locate main table


# f = open('/Applications/MAMP/htdocs/urlwatch/tha.png','wb')
# f.write(requests.get('http://xn--42c2bi7an0cb9p.com/images/flag/tha.png').content)
# f.close()



# pip install urllib
data = []
for obj in main_table.find_all('tr',{'class': 'underline'}):
    row = {}
    ac_list = [x.text.encode("utf-8").strip() for x in obj.find_all('td',{'class':'ac'})]
    nc = obj.find('td',{'class': 'name'})
    name_img = nc.find('img',{'class': 'player-img'})['src'].encode("utf-8")

    row['player-img'] = name_img.rsplit('/', 1)[-1]
    row['complete_name'] = obj.find('td',{'class': 'name'}).text.encode('utf-8').strip()
    row['time_attendance'] = ac_list[0]
    row['score'] = ac_list[1]
    row['team_name'] = obj.find('td',{'class': 'al'}).text.encode('utf-8').strip()

    if not check_file_exist(local_flag_image_directory+row['player-img']):
        url_file_to_download = domain+name_img
        local_file_to_download = local_flag_image_directory+row['player-img']
        download_file_to_directory(url_file_to_download , local_file_to_download)

    data.append(row)

print json.dumps(data, indent = 5)