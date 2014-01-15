from bs4 import BeautifulSoup;
import re;
import urllib.request;
import pickle
import time
from math import floor
from math import ceil
import random

def get_proxies():
    url = 'http://proxy-hunter.blogspot.com/2010/03/18-03-10-speed-l1-hunter-proxies-310.html'
    document = urllib.request.urlopen(url)
    tree = BeautifulSoup(document.read())
    regex  = re.compile(r'^(\d{3}).(\d{1,3}).(\d{1,3}).(\d{1,3}):(\d{2,4})')
    data = []
    #proxylist = tree.findAll(attrs = {"class":"Apple-style-span", "style": "color: black;"}, text = regex)
    for tag in tree.findAll(attrs = {"class":"Apple-style-span", "style": "color: black;"}, text = regex):
        data += [tag.text]
    
    return data[0].split('\n')
proxy_num = 1
#proxies = get_proxies()
#proxies_len = len(proxies)
#print (proxies, proxies_len)


Lecture_div_no= range(1,16)
div_sub_list = {}
div_sub_list_fname = "divSL_dump"
strength_map = {}
strength_map_fname = "strength_dump"
lecture_map = {}
lecture_map_fname = "lectureM_dump"

lecture_to_sgf_map = {}
lecture_to_sgf_fname = "lecture_sgf_dump"

pages_cache_folder = "pages"
sgf_cache_folder = "ctf_cache"
page_encoding = 'euc-kr'
use_proxy = True

#http://www.wbaduk.com/FileUpDown/lecture/0301-maeksu018.ctf
proxy = None
auth = None
ctfTable = []
page_per_block = 10
wait_time = 5
download_last_time = time.time()
main_page_url_begin = "http://www.wbaduk.com/lecture/lecture_text.asp?"
lecture_page_url_begin = "http://www.wbaduk.com/lecture/lecture_text_view.asp?"
sgf_file_begin_link = "http://www.wbaduk.com/FileUpDown/lecture/"

div_pattern = re.compile("Lecture_Sub_No=\d+&mode=\d+$", re.IGNORECASE)


div_last_page_pattern = re.compile("&pageNo=\d+&blockNo=\d+$", re.IGNORECASE)
div_last_page_pattern_detail = re.compile("&pageNo=(?P<page_no>\d+)&blockNo=(?P<block_no>\d+)$", re.IGNORECASE)

strength_div_patt = re.compile("Lecture_div_no=\d+&mode=\d$", re.IGNORECASE)
strength_detail_patt = re.compile("Lecture_div_no=(?P<div_no>\d+)&mode=\d$", re.IGNORECASE)

lec_patt = re.compile("Lecture_div_no=(?P<div_no>\d+)&Lecture_Sub_No=(?P<sub_no>\d+)&mode=(?P<mode>\d+)", re.IGNORECASE)

lec_link_patt = re.compile("JavaScript:Lecture_load", re.IGNORECASE)
lec_link_patt_detail = re.compile("JavaScript:Lecture_load\(\'(?P<lec_num>\d+)\'\);", re.IGNORECASE)
lecture_to_sgf_map = {}
lecture_to_sgf_fname = "lecture_sgf_dump"

def readPageFromDisc(url_begin, url, cache_folder, fExt):
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
        #load_proxy(proxy_num)
        #proxy_num += 1
        page = urllib.request.urlopen(fullurl)
        download_last_time = time.time()
        page_from_url = page.read().decode(page_encoding)
        with open(filename, mode='w', encoding = page_encoding) as a_file:
            a_file.write(page_from_url)
            return page_from_url
    

def setup_urllib():
    if use_proxy:
        proxy  = urllib.request.ProxyHandler({'http': 'http://user:password@proxy_address:8080'})
        auth = urllib.request.HTTPBasicAuthHandler()
        opener = urllib.request.build_opener(proxy, auth, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)

def load_proxy(num):
    #proxies = get_proxies()
    #proxies_len = len(proxies)
    proxy = urllib.request.ProxyHandler({'http': 'http://' + proxies[num % proxies_len]})
    auth = urllib.request.HTTPBasicAuthHandler()
    opener = urllib.request.build_opener(proxy, auth, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
        
def load_main_page(lec_div_no, lec_sub_no=None, mode=None, pageNo=None, blockNo=None):
    url = "Lecture_div_no="+str(lec_div_no)+\
            ("&Lecture_Sub_No=" + str(lec_sub_no))* (lec_sub_no is not None) + ("&mode=" + str(mode)) * (mode is not None) +\
            ("&pageNo="+ str(pageNo)) * (pageNo is not None) + ("&blockNo=" + str(blockNo)) * (blockNo is not None) 
    return readPageFromDisc(main_page_url_begin, url,pages_cache_folder, ".html")

def load_lecture_page(l_num):
    url = "lecture_no=" + str(l_num) 
    return readPageFromDisc(lecture_page_url_begin, url, pages_cache_folder, ".html")

def load_sgf_file(sgf_filename):
    if link_contains_chars_outsiderange(sgf_filename):
        print(sgf_filename, "contains chars outside of 128 range")
        return None
    url = sgf_filename
    return readPageFromDisc(sgf_file_begin_link, url, sgf_cache_folder, "")

def extract_data_from_page(l_num):
    if l_num in lecture_to_sgf_map:
        return lecture_to_sgf_map[l_num]
    else:
        page = load_lecture_page(l_num)
        tit_m = re.search(r'<param\s*name="title"\s+value="(?P<title>[^">]*)">', page)
        lec_m = re.search(r'<param\s*name="lecture"\s+value="(?P<lecture>[^">]*)">', page)
        #lecture_match = re.search(r'(<param\s*name="lecture"[^>]*)', page)
        if tit_m and lec_m:
            lecture_to_sgf_map[l_num] = tit_m.group('title'), lec_m.group('lecture'), extract_sgf_name(lec_m.group('lecture'))
           
    

def extract_sgf_name(lecturelink):
    #for tag in dec_soup.find_all(href=re.compile("Lecture_Sub_No")):
    info_m = re.search(r'(?P<main>.*lecture\/)(?P<ctf_file>.*\.ctf)', lecturelink)
    if info_m:
        return info_m.group('ctf_file')

def extract_sub_list(div_no):
    page= load_main_page(div_no)
    dec_soup = BeautifulSoup(page)
    div_sub_list[int(div_no)] = {}
    for tag in dec_soup.find_all(href=div_pattern):
        #print(tag.text + '##' + tag.attrs['href'] + '\n')
        lec_m = re.search(lec_patt, tag.attrs['href'])  
        if lec_m: pass
            #print(lec_m.groups())
        else:
            print("No match for " + str(div_no))
        div_no, sub_no = int(lec_m.group('div_no')), int(lec_m.group('sub_no'))
        div_sub_list[div_no][sub_no] = [tag.text]
        
        
def extract_max_page(div_no, sub_no):
    #div_last_page_pattern_detail = re.compile("&pageNo=(?P<page_no>\d+)&blockNo=(?P<block_no>\d+)$")
    page = load_main_page(div_no, sub_no)
    dec_soup = BeautifulSoup(page)
    paging_high = 0
    block_high = 0
    paging_current = 0
    for link in dec_soup.find_all(href=div_last_page_pattern):
        #print (link)
        #print('##' + link.attrs['href'] + '\n')
        page_m = re.search(div_last_page_pattern_detail, link.attrs['href'])
        if page_m :
            page_no, block_no = int(page_m.group('page_no')), int(page_m.group('block_no'))
            paging_high, block_high = max(paging_high, page_no), max(block_high, block_no)
            
    div_sub_list[div_no][sub_no] += [paging_high, block_high]        
    
    

def extract_strength_list(page):
    dec_soup = BeautifulSoup(page)
    global strength_map
    for tag in dec_soup.find_all(href=strength_div_patt):
        #print(tag.text + '##' + tag.attrs['href'] + '\n')
        strength_m = re.search(strength_detail_patt, tag.attrs['href'])
        if strength_m:
            #print(strength_m.groups())
            strength_map[int(strength_m.group('div_no'))]= tag.text
        else:
            print("No match for page")
            strength_map[int(strength_m.group('div_no'))]= strength_m.group('div_no')
        
def extract_lecture_numbers():
    max_p = 10
    i = 1
    for div_no in div_sub_list:
        if div_no not in lecture_map:
            lecture_map[div_no] = {}
        for sub_no in div_sub_list[div_no]:
            name, max_page, max_block = div_sub_list[div_no][sub_no]
            #print(name, max_page, max_block)
            if sub_no not in lecture_map[div_no]:
                lecture_map[div_no][sub_no] = []
            if max_page > 0:
                for page_num in range(1, max_page + 1):
                    #if i > max_p:
                    #    return
                    #else:
                    #    i = i + 1
                    #def load_main_page(lec_div_no, lec_sub_no=None, mode=None, pageNo=None, blockNo=None):
                    page = load_main_page(div_no, sub_no, None, page_num, ceil(page_num /page_per_block))
                    dec_soup = BeautifulSoup(page)
                    for link in dec_soup.find_all("td", style="padding:0 5 0 5"):
                        aa = link.find("a")
                        #print (link, '\n\n', aa)
                    
                        lec_m = re.search(lec_link_patt_detail, aa.attrs['href'])
                        #print (lec_m, aa.attrs['href'])
                        if lec_m:
                            lecture_map[div_no][sub_no] += [[int(lec_m.group('lec_num')), aa.text]]  
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
def link_contains_chars_outsiderange(s):
    return any([ord(x) > 128 for x in s])

def extract_all_data():
    print("extracting data " )
    for div_no in lecture_map:
        for sub_no in lecture_map[div_no]:
            for item in lecture_map[div_no][sub_no]:            
                extract_data_from_page(item[0])
    with open(lecture_to_sgf_fname,'wb') as ff:
        pickle.dump(lecture_to_sgf_map, ff)
    problem_count = 0
    lec_set = set()
    for div_no in lecture_map:
        for sub_no in lecture_map[div_no]:
           for item in lecture_map[div_no][sub_no]:
               problem_count += 1
               lec_set.add(item[0])
    print("total problem count is " + str(problem_count))
    print("total unique problem count is " + str(len(lec_set)))

def extract_problems():
    prob_count = 0
    for key in lecture_to_sgf_map:
        prob_count += 1
        load_sgf_file(lecture_to_sgf_map[key][2])
        print ("Extracting problem number " + str(prob_count))
        
def setup_all():
    setup_urllib()
    div_no = 1
    global strength_map
    global div_sub_list
    global lecture_map
    global lecture_to_sgf_map
    
    print("opening " + strength_map_fname)
    try:
        with open(strength_map_fname,'rb') as f:
            strength_map = pickle.load(f)
            print("opening " + strength_map_fname + "succeded")
    except IOError as e:
        workpage = load_main_page(div_no)
        extract_strength_list(workpage)
        print("opening " + strength_map_fname + "failed")
        with open(strength_map_fname,'wb') as ff:
            pickle.dump(strength_map, ff)
    print("opening " + div_sub_list_fname)
    try:
        with open(div_sub_list_fname,'rb') as f:
            div_sub_list = pickle.load(f)
            print("opening " + div_sub_list_fname + "succeded")
    except IOError as e:
        print("opening " + div_sub_list_fname + "failed")
        for div_no in Lecture_div_no:
            print("Extracting info from div_no =" + str(div_no))
            workpage  = load_main_page(div_no)
            extract_sub_list(div_no)
        for div_no in Lecture_div_no:
            for sub_no in div_sub_list[div_no]:
                print("examinig: ", div_no, sub_no, div_sub_list[div_no][sub_no])
                extract_max_page(div_no, sub_no)
        with open(div_sub_list_fname,'wb') as ff:
            pickle.dump(div_sub_list, ff)
    print("opening " + lecture_map_fname)
    try:
        with open(lecture_map_fname,'rb') as f:
            print("opening " + lecture_map_fname + "succeded")
            lecture_map = pickle.load(f)
    except IOError as e:
        print("opening " + lecture_map_fname + "failed")
        extract_lecture_numbers()
        with open(lecture_map_fname,'wb') as ff:
            pickle.dump(lecture_map, ff)
    print("opening " + lecture_to_sgf_fname)
    try:
        with open(lecture_to_sgf_fname,'rb') as f:
            print("opening " + lecture_to_sgf_fname + "succeded")
            lecture_to_sgf_map = pickle.load(f)
            
    except IOError as e: print("opening " + lecture_to_sgf_fname + "succeded")
    #print(lecture_map[1])

lecture_ctf_list_fname="lecture_ctf_ListDump.txt"

def createlecture_to_sgfList():
    #print(len(lecture_map))
    sgfList = [str(it) for it in sorted(item for item in lecture_to_sgf_map.items())]
    #sgfList = sorted([str(item) for item in list(lecture_to_sgf_map.items())])
    sgfString = '\n'.join(sgfList)
    print(sgfString[:400])
    #print(sgfList)
    with open(lecture_ctf_list_fname,'wt', encoding='utf-8') as ff:
            ff.write(sgfString)



                      
if __name__=="__main__":
    
    #page = load_lecture_page(1066)
    #print(page + '\n----------------')
    #extracted_l = extract_data_from_page(page)
    #extracted_l = extract_data_from_page(test_page)
    #print(extracted_l)
    setup_all()
    createlecture_to_sgfList()
    #extract_all_data()
    #extract_problems()
        
    #print(lecture_to_sgf_map)
    #load_sgf_file("0301-maeksu018.ctf")
    #extract_data_from_page(222)
        #if(aa):
        #    print (link, aa)
        #print('##' + link.attrs['href'] + '\n')
    #print (lecture_map[4])
    #print(lecture_to_sgf_map)
    #print(div_sub_list)
    #print(strength_map)
    
    
    
    

#patt = (b'(<param[^>]+)', b'\1/>')



#page = urllib.request.urlopen("http://www.wbaduk.com/FileUpDown/lecture/0604-choisu095.ctf1.ctf")
#ll = re.findall(b'(<param name="lecture"[^>]*)', read_page)
#ll[0].decode("utf-8")

#print(page.read())
#soup = BeautifulSoup(page.read())
#print(soup)
