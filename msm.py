
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time
import hashlib
from db import insert_into_post


def getPageData():
    print("Invoked")
    url = "https://m.facebook.com/PlayMapleM/posts"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1124x850")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--test-type")
    driver = webdriver.Chrome(chrome_options = chrome_options,service_args=["--verbose", "--log-path=./chromedriver.log"], executable_path="./chromedriver")
    driver.get(url)
    return driver

def parsePageData(driver):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source,'html.parser')
    posts = soup.findAll('div',{'class':'story_body_container'})
    for p in posts:
        post_text = p.text
        if re.search("... More", post_text):
            url = p.find("span",{"data-sigil":"more"})
            link = url.find('a')
            parseNestedPageData(driver,link['href'])

        else: 
            post_val =format_text(post_text)
            insert_into_post(post_val,sha256(post_val))
            

    driver.close()

def parseNestedPageData(driver,url):
    nested_url = "https://m.facebook.com{}".format(url)
    driver.get(nested_url)
    time.sleep(1)
    nested_ps = driver.page_source
    soup2 = BeautifulSoup(nested_ps,'html.parser')
    msg = soup2.find('div',{'class':'msg'})
    try:
        post_val = format_text(msg.text)
        insert_into_post(post_val,sha256(post_val))
        
        
    except AttributeError:
        msg = soup2.find('div',{'data-ad-preview':'message'})
        try:
            post_val =format_text(msg.text)
            insert_into_post(post_val,sha256(post_val))
            
        except AttributeError:
            pass

def format_text(text_to_format):
    list_split_dots = re.split('•',text_to_format)
    list_split_dots = [x.lstrip() for x in list_split_dots]
    # reconcat the string.
    string_split_dots = "\n- ".join(list_split_dots)
    # splits by " " more than 1 space to new line
    output = re.split(r'\s{2,}', string_split_dots)
    split_string_spaces = '\n'.join(output)
    # we split by >2 spaces.
    # let just now handle ========
    output = re.split(r'={3,}', split_string_spaces)
    split_string_equals = '\n=============================\n'.join(x.strip() for x in output)
    # handles another 
    # pls no more nexon.
    split_string_equals = re.sub(r'^MapleStory M', '', split_string_equals)
    return split_string_equals


def sha256(string_to_hash):
    return hashlib.sha256(string_to_hash.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    parsePageData(getPageData())
    print("Done")