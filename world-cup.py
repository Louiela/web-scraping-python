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
local_flag_image_directory = '/Users/lou.dulguime/Documents/Projects/python/bkk/images/country-flag/'


url_to_scrape = 'http://xn--42c2bi7an0cb9p.com/nationtable.php'
r = requests.get(url_to_scrape) # get html source
soup = BeautifulSoup(r.text,'html.parser') # parsing data to BeautifulSoup
main_table = soup.select_one("table:nth-of-type(1)") # locate main table


itable = main_table.find_all('tr')
itable_td = itable[1]
inner_table = itable_td.find('table')

data = []
for obj in inner_table.find_all('tr',style=True):
    row = {}
    home_comming = {}
    visit = {}
    total = {}
    td_list = obj.find_all('td',{'valign':'middle'})
    team_img = td_list[1].find('img')['src'].encode("utf-8")
    team_name = td_list[1].text.encode("utf-8").strip()
    home_comming['won'] = td_list[2].text.encode("utf-8").strip()
    home_comming['drawn'] = td_list[3].text.encode("utf-8").strip()
    home_comming['lost'] = td_list[4].text.encode("utf-8").strip()
    home_comming['goals_scored'] = td_list[5].text.encode("utf-8").strip()
    home_comming['goals_against'] = td_list[6].text.encode("utf-8").strip()
    visit['won'] = td_list[7].text.encode("utf-8").strip()
    visit['drawn'] = td_list[8].text.encode("utf-8").strip()
    visit['lost'] = td_list[9].text.encode("utf-8").strip()
    visit['goals_scored'] = td_list[10].text.encode("utf-8").strip()
    visit['goals_against'] = td_list[11].text.encode("utf-8").strip()
    total['game_played'] = td_list[12].text.encode("utf-8").strip()
    total['won'] = td_list[13].text.encode("utf-8").strip()
    total['drawn'] = td_list[14].text.encode("utf-8").strip()
    total['lost'] = td_list[15].text.encode("utf-8").strip()
    total['goals_scored'] = td_list[16].text.encode("utf-8").strip()
    total['goals_against'] = td_list[17].text.encode("utf-8").strip()
    total['points'] = td_list[18].text.encode("utf-8").strip()
    row['team_name'] = team_name
    row['team_flag'] = team_img.rsplit('/', 1)[-1]
    row['home_comming'] = home_comming
    row['visit'] = visit
    row['total'] = total
    if not check_file_exist(local_flag_image_directory+row['team_flag']):
        url_file_to_download = domain+team_img
        local_file_to_download = local_flag_image_directory+row['team_flag']
        download_file_to_directory(url_file_to_download , local_file_to_download)
    data.append(row)


print json.dumps(data, indent = 5)