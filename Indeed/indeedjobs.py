from bs4 import BeautifulSoup
import pandas as pd
import requests
from functools import reduce
from selenium import webdriver
from urllib.parse import urlparse
driver=webdriver.Chrome("C:/webdrivers/chromedriver.exe")
my_url='https://www.indeed.com/jobs?as_and=.net+developer&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=contract&st=&as_src=&salary=&radius=25&fromage=1&limit=10&sort=date&psf=advsrch&from=advancedsearch'
driver.get(my_url)
res=driver.execute_script("return document.documentElement.outerHTML")
driver.quit()
page_soup=BeautifulSoup(res,"html.parser")

def position(page_soup):
    positions=[]
    for div in page_soup.find_all(name="div", attrs={"class":"jobsearch-SerpJobCard"}):
        for d in div.find_all(name="div", attrs={"class":"title"}):
            for a in d.find_all(name="a", attrs={"class":"jobtitle"}):
                positions.append(a['title'])
    return positions
x=list(position(page_soup))
print(len(x))
def company(page_soup):
    companies=[]
    for div in page_soup.find_all(name="div", attrs={"class":"jobsearch-SerpJobCard"}):
        for d in div.find_all(name="div", attrs={"class":"sjcl"}):
            for span in d.find_all(name="span", attrs={"class":"company"}):
                companies.append(span.text.strip())
    return companies
y=list(company(page_soup))
print(len(y))
def location(page_soup):
    locations=[]
    for div in page_soup.find_all(name="div", attrs={"class": "jobsearch-SerpJobCard"}):
        for di in div.find_all(name="div", attrs={"class": "sjcl"}):
             for d in di.find_all(name="div", attrs={"class":"recJobLoc"}):
                 locations.append(d['data-rc-loc'])

    return locations
z=list(location(page_soup))
print(len(z))

def date(page_soup):
    dates=[]
    for div in page_soup.find_all(name="div",attrs={"class":"jobsearch-SerpJobCard"}):
        for di in div.find_all(name="div", attrs={"class":"jobsearch-SerpJobCard-footer"}):
            for d in di.find_all(name="div",attrs={"class":"result-link-bar"}):

                for span in d.find_all(name="span",attrs={"class":"date"}):
                    dates.append(span.text)

    return dates
d=list(date(page_soup))
print(len(d))

def link(page_soup):
    weblinks=[]
    for div in page_soup.find_all(name="div", attrs={"class":"jobsearch-SerpJobCard"}):
        for d in div.find_all(name="div", attrs={"class":"title"}):

            links=d.find("a", {"class":"jobtitle"}).get('href')
            website="https://www.indeed.com"
            weblinks.append(website+str(links))
    return weblinks
a=list(link(page_soup))
print(len(a))

m = []
n = []
o = []
p = []
q = []

def pagination(page_soup):
   pages = []
   
   for div in page_soup.find_all(name="div", attrs={"class": "pagination"}):
      for a in div.find_all(name="a"):
          for span in a.find_all(name="span", attrs={"class": "np"}):

            if "Next" in span.text:

                    website = "https://www.indeed.com"
                    url_tag = a.get('href')
                    pages=(website + str(url_tag))
                    d = webdriver.Chrome("C:/webdrivers/chromedriver.exe")
                    d.get(pages)
                    response = d.execute_script("return document.documentElement.outerHTML")
                    d.quit()
                    newpage = BeautifulSoup(response, 'html.parser')
                    m.append(position(newpage))
                    n.append(company(newpage))
                    o.append(location(newpage))
                    q.append(date(newpage))
                    p.append(link(newpage))
                    pagination(newpage)

            else:
                    break
   return m, n, o, q, p


t = pagination(page_soup)
print(t)
pos = []
com = []
loc = []
dat = []
webl = []
pos = reduce(lambda x, y: x + y, t[0])
com = reduce(lambda x, y: x + y, t[1])
loc = reduce(lambda x, y: x + y, t[2])
dat = reduce(lambda x, y: x + y, t[3])
webl = reduce(lambda x, y: x + y, t[4])

zippedList = list(zip(x+pos,y+com,z+loc,d+dat,a+webl))
dfObj=pd.DataFrame(zippedList,columns=['position','Company','Location','Date','link'])
s=pd.DataFrame(dfObj).to_csv('outputindeedjobs.csv',header=True,index=None)
print(s)




