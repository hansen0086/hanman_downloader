import requests
import re
import os
import sys
import math
from tqdm import tqdm
from bs4 import BeautifulSoup
import urllib
import shutil


def getHTMLText(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'}
        r = requests.get(url, timeout=1000, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Error in status"


#wrapper = soup.find('div', id='comicpage')

def get_image(url, title):
    text = getHTMLText(url)
    soup = BeautifulSoup(text, 'lxml')
    folder_name = soup.find('title').get_text().split('-')[0].strip()
    folder_name = title+"/"+folder_name
    print('downlaoding:'+folder_name)
    try:
        os.mkdir(folder_name)
    except:
        print("folder already exists")
    target = soup.findAll('img', class_='lazy')
    image_links = [each.get('data-original') for each in target]
    # print(image_links)
    for each in image_links:
        print("trying downlaod " + each)
        filename = each.split('/')[-1]
        r = requests.get(each, stream=True)
        if r.status_code == 200:
            with open(folder_name+'/'+filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

    return image_links


def get_next_url(url):
    text = getHTMLText(url)
    soup = BeautifulSoup(text, 'lxml')
    soup.prettify()
    # print(soup.findAll("li")[-1])
    next = soup.findAll("li")[-1].a['href']
    if (next):
        target = "http://www.jjmhw.cc" + next
        return target
    else:
        return -1


def getFirstUrl(keyword):
    # keyword = input("Enter keyword: ")
    search_url = "http://www.jjmhw.cc/search?keyword="+keyword
    search_text = getHTMLText(search_url)
    soup = BeautifulSoup(search_text, 'lxml')
    soup.prettify()
    ref = soup.findAll("li")[0].a['href']
    next_url = "http://www.jjmhw.cc" + ref
    next_text = getHTMLText(next_url)
    soup = BeautifulSoup(next_text, 'lxml')
    soup.prettify()
    first = soup.findAll("li")[0].a['href']
    return "http://www.jjmhw.cc" + first


def getFirstTitle(keyword):
    search_url = "http://www.jjmhw.cc/search?keyword="+keyword
    search_text = getHTMLText(search_url)
    soup = BeautifulSoup(search_text, 'lxml')
    soup.prettify()
    return soup.findAll("li")[-1].a['title']


# main starts here:
keyword = input("Enter keyword: ")
domain = "http://www.jjmhw.cc"
title = getFirstTitle(keyword)
print(title+" found")
os.mkdir(title)

base_url = getFirstUrl(keyword)


current_url = base_url

while(True):
    # get_image(current_url)
    next_url = get_next_url(current_url)
    if(next_url != -1):
        get_image(current_url, title)
        # print(current_url)
        current_url = next_url
    else:
        break
