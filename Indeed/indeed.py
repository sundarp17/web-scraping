import bs4
import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
from urllib.request import urlopen as ureq
from functools import reduce

url="https://www.indeed.com/jobs?as_and=.net+developer&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=contract&st=&as_src=&salary=&radius=25&fromage=1&limit=10&sort=date&psf=advsrch&from=advancedsearch"
uclient = ureq(url)
page_html = uclient.read()
uclient.close()
page_soup = soup(page_html, "html.parser")

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


def pagination(page_soup):
    pages = []
    new_soup = []
    condition= page_soup.find_all(name="div",attrs={"class":"relatedQuerySpacing"})
    if condition==[]:
      for div in page_soup.find_all(name="div", attrs={"class": "pagination"}):
        for a in div.find_all(name="a"):
            for span in a.find_all(name="span", attrs={"class": "np"}):
                if "»" in span.text:

                    website = "https://www.indeed.com"

                    url_tag = a.get('href')
                    pages.append(website + str(url_tag))

                    for pg in pages:
                        response = requests.get(pg)
                        data = response.text
                        new_soup.append(soup(data, "html.parser"))
                        for newpage in new_soup:
                            m.append(position(newpage))
                            n.append(company(newpage))
                            o.append(location(newpage))
                            p.append(link(newpage))
                            print(pg)
                            pagination(newpage)

                else:
                    break
    return m, n, o, p


t = pagination(page_soup)
print(t)
pos = []
com = []
loc = []
webl = []
pos = reduce(lambda x, y: x + y, t[0])
com = reduce(lambda x, y: x + y, t[1])
loc = reduce(lambda x, y: x + y, t[2])
webl = reduce(lambda x, y: x + y, t[3])

zippedList = list(zip(x+pos,y+com,z+loc,a+webl))
dfObj=pd.DataFrame(zippedList,columns=['position','Company','Location','link'])
s=pd.DataFrame(dfObj).to_csv('outputindeed.csv',header=True,index=None)
print(s)