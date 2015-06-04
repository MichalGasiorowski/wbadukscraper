from bs4 import BeautifulSoup;
import re;
import urllib.request;
import requests
import time
import os.path
import random

main_page_url_begin = "http://www.wbaduk.com/lecture/lecture_text.asp?"
lecture_page_url_begin = "http://www.wbaduk.com/lecture/lecture_text_view.asp?"
sgf_file_begin_link = "http://www.wbaduk.com/FileUpDown/lecture/"
wait_time = 1
download_last_time = time.time()
page_encoding = 'euc-kr'
pages_cache_folder = "pages"
sgf_cache_folder = "ctf_cache"

def link_contains_chars_outsiderange(s):
    return any([ord(x) > 128 for x in s])

def extract_sgf_name(lecturelink):
    info_m = re.search(r'(?P<main>.*lecture\/)(?P<ctf_file>.*\.ctf)', lecturelink)
    if info_m:
        return info_m.group('ctf_file')

def readPageFromDisc(url_begin, url, cache_folder, fExt):
    if not os.path.exists(pages_cache_folder) :
        os.mkdir(pages_cache_folder)
                            
    fullurl = url_begin + url;
    filename = cache_folder + "/" + url + fExt#".html"
    global download_last_time
    try:
        with open(filename) as cached_page:
            print("Getting page with " + fullurl + " from disc\n")
            return cached_page.read()
    except IOError:
        now = time.time()
        sub_time = now - download_last_time - random.random()/4
        if sub_time < wait_time:
            print("Waiting for " + str(wait_time - sub_time) + " seconds")
            time.sleep(wait_time - sub_time)
        print("Getting page with " + fullurl + " from internet\n")
        r = requests.get(fullurl)
        r.encoding = page_encoding
        download_last_time = time.time()
        #page_from_url = page.read().decode(page_encoding)
        page_from_url = r.text
        
        with open(filename, mode='w', encoding = page_encoding, errors='replace') as a_file:
            a_file.write(page_from_url)
            return page_from_url
        
def load_sgf_file(sgf_filename):
    if link_contains_chars_outsiderange(sgf_filename):
        print(sgf_filename, "contains chars outside of 128 range")
        return None
    url = sgf_filename
    return readPageFromDisc(sgf_file_begin_link, url, sgf_cache_folder, "")

def extract_data_from_page(l_num):
    page = load_lecture_page(l_num)
    tit_m = re.search(r'<param\s*name="title"\s+value="(?P<title>[^">]*)">', page)
    lec_m = re.search(r'<param\s*name="lecture"\s+value="(?P<lecture>[^">]*)">', page)
    #if tit_m and lec_m:
        #return tit_m.group('title'), lec_m.group('lecture'), extract_sgf_name(lec_m.group('lecture'))
    if tit_m and lec_m:
        return extract_sgf_name(lec_m.group('lecture'))
           
def load_lecture_page(l_num):
    url = "lecture_no=" + str(l_num) 
    return readPageFromDisc(lecture_page_url_begin, url, pages_cache_folder, ".html")


for lec in range(1, 13000):
    sgf_name = extract_data_from_page(lec)
    if sgf_name:
        sgf = load_sgf_file(sgf_name)
