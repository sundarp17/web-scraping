from bs4 import BeautifulSoup
import pandas as pd
import requests
from functools import reduce
from selenium import webdriver
from urllib.parse import urlparse
driver=webdriver.Chrome("C:/webdrivers/chromedriver.exe")
my_url='https://www.dice.com/jobs?q=php%20developer&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=20&filters.postedDate=ONE&filters.employmentType=THIRD_PARTY&language=en'
driver.get(my_url)
res=driver.execute_script("return document.documentElement.outerHTML")
driver.quit()
soup=BeautifulSoup(res,"html.parser")
newurl=my_url.split("1")

def position(soup):
    jobs=[]
    for div in soup.find_all(name="div",attrs={"class":"title-container"}):
        for a in div.find_all(name="a",attrs={"class":"card-title-link bold"}):

            jobs.append(a.text)
    return(jobs)


def company(soup):
    companys=[]
    for div in soup.find_all(name="div", attrs={"class":"card-company"}):
        for a in div.find_all(name="a", attrs={"data-cy":"search-result-company-name"}):
            companys.append(a.text)
    return(companys)


def location(soup):
    location=[]
    for div in soup.find_all(name="div",attrs={"class":"card-company"}):
        for span in div.find_all(name="span"):
            location.append(span.text)
    return(location)

def weblink(soup):
    weblinks=[]
    for div in soup.find_all(name="div",attrs={"class":"title-container"}):
        for links in div.find_all(name="a",attrs={"class":"card-title-link"}):
           weblinks.append(links.get('href'))

    return(weblinks)


def jobid(soup):
    newlink=[]
    jobids=[]
    for div in soup.find_all(name="div",attrs={"class":"title-container"}):
        for links in div.find_all(name="a",attrs={"class":"card-title-link"}):
            newlink.append(links.get('href'))

    for nl in newlink:
        job_response=requests.get(nl)
        job_data=job_response.text
        jobids.append(BeautifulSoup(job_data, "html.parser"))

    id=[]

    for ids in jobids:
        for div in ids.find_all(name="div",attrs={"class":"company-header-info"}):
            for d in div.select('.company-header-info > div:nth-of-type(3)'):
                for t in d.find_all(name="div",attrs={"class":"col-md-12"}):
                    if "Position" in t.text:
                        id.append(t.text)
                    else:
                        for d in div.select('.company-header-info > div:nth-of-type(2)'):
                            for t in d.find_all(name="div", attrs={"class": "col-md-12"}):
                                id.append(t.text)
    return id

def position_type(soup):
    newlinks=[]
    types=[]
    for div in soup.find_all(name="div",attrs={"class":"title-container"}):
        for links in div.find_all(name="a",attrs={"class":"card-title-link"}):
            newlinks.append(links.get('href'))
    for nl in newlinks:
        job_response=requests.get(nl)
        job_data=job_response.text
        types.append(BeautifulSoup(job_data, "html.parser"))
    type=[]

    for ty in types:
        for div in ty.find_all(name="div",attrs={"class":"container job-details"}):
            for di in div.find_all(name="div",attrs={"class":"col-md-8"}):
                for d in di.find_all(name="input",attrs={"id":"taxTermsTextId"}):
                    type.append(d.get('value'))

    return type


span = soup.find("span", {"id": "totalJobCount"})

n=(span.text)
print(n)
count=(int(n)//20)
print(count)
m=[]
n=[]
o=[]
p=[]
q=[]
r=[]
def pagination(soup):


    for i in range(1,count+2):

        url =newurl[0]+str(i)+newurl[1]
        
        d = webdriver.Chrome("C:/webdrivers/chromedriver.exe")
        d.get(url)
        response = d.execute_script("return document.documentElement.outerHTML")
        d.quit()
        bs=BeautifulSoup(response,'html.parser')
        m.append(position(bs))
        n.append(company(bs))
        o.append(location(bs))
        p.append(weblink(bs))
        q.append(jobid(bs))
        r.append(position_type(bs))
    return m,n,o,p,q,r
pag=pagination(soup)

loc=reduce(lambda x,y:x+y,pag[0])
pos=reduce(lambda x,y:x+y,pag[1])
com=reduce(lambda x,y:x+y,pag[2])
webl=reduce(lambda x,y:x+y,pag[3])
jid=reduce(lambda x,y:x+y,pag[4])
ptype=reduce(lambda x,y:x+y,pag[5])


zippedList=list(zip(loc,pos,com,webl,jid,ptype))
dfObj=pd.DataFrame(zippedList,columns=['position','Company','location','weblink','Job ID','Position Type'])
print(dfObj, sep='\n')

ex=pd.DataFrame(dfObj).to_csv('outputdice.csv',header=True,index=None)
print(ex)
