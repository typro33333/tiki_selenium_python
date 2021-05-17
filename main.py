from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json, queue, time
from threading import Thread
import pandas as pd
#setup contrain
o = webdriver.ChromeOptions()
#-----------------------------------
##IF run on window need chromedriver.exe
o.add_argument("./chromedriver.exe") ## Version chorme now is  90.0.4430.212
##-----------------------------------
o.add_argument("disable-features=VizDisplayCompositor")
o.add_argument("headless")
o.add_argument("window-size=1200x800")
o.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0")
driver = webdriver.Chrome(options=o)
action = webdriver.ActionChains(driver)
#crawling
driver.get("https://tiki.vn/laptop/c8095")
time.sleep(0.5)
#get all product urls
items = driver.find_elements_by_class_name("product-item")
urls = []
for i in range(len(items)):
    urls.append(items[i].get_attribute("href"))
#check number of url
print("number of products:",len(urls))
#crawling function
def get_data(url,driver):
    time.sleep(2)
    driver.get(url)
    data = {}
    title = driver.find_element_by_class_name("title").text
    price = driver.find_element_by_class_name("product-price__current-price").text
    image = driver.find_element_by_xpath("/html/body/div[1]/div[1]/main/div[4]/div/div[1]/div[1]/div[1]/div/div/div/div/img").get_attribute("src")
    description = driver.find_element_by_xpath("/html/body/div[1]/div[1]/main/div[6]/div/div[1]/div[2]/div/div/div/div").text
    detail = {}
    for i in range(len(driver.find_elements_by_xpath("//table/tbody/tr"))):
        detail.update({driver.find_element_by_xpath("//tr["+str(i+1)+"]/td[1]").text:driver.find_element_by_xpath("//tr["+str(i+1)+"]/td[2]").text})
    data.update({
        "title":title,
        "price":price,
        "images":image,
        "description":description,
        "detail":detail
        })
    return data

#exe
result = []
for url in urls:
    try:
        result.append(get_data(url,driver))
    except:
        pass
#rename here
file_name = "./test1.json"
json.dump(result,open(file_name,"w"))

#Readfile json again
f = open('./test1.json',)
r = json.load(f)

data = []
for i in r: 
    data.append(i)

for i in range(len(data)):
    data[i].update(data[i]['detail'])
    del data[i]['detail']

file_name = "./data.json"
json.dump(data,open(file_name,"w"))

#Export json file to csv data
df = pd.read_json(r'.\data.json')
df.to_csv(r'.\data.csv')

driver.close()