import bs4
import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
from urllib.request import urlopen as ureq
from functools import reduce


my_url = "https://www.careerbuilder.com/jobs?posted=1&pay=&cat1=&radius=&emp=jtct%2Cjtfl%2Cjtc2%2Cjtcc&cb_apply=false&cb_workhome=false&keywords=.Net+Developer&location="
uclient = ureq(my_url)
page_html = uclient.read()
uclient.close()
page_soup = soup(page_html, "html.parser")


def position(page_soup):
    positions = []
    for jobs in page_soup.find_all(name="div", attrs={"class": "data-results-content-parent relative"}):
        for div in jobs.find_all(name="div", attrs={"class": "data-results-title"}):
            positions.append(div.text)
    return (positions)
x=list(position(page_soup))
print(x)

def location(page_soup):
    locations = []
    for jobs in page_soup.find_all(name="div", attrs={"class": "data-results-content-parent relative"}):
        for div in jobs.findAll('div', {'class': 'data-details'}):
            for span in div.select('.data-details > span:nth-of-type(2)'):
                locations.append(span.text)
    return (locations)
y=list(location(page_soup))

def company(page_soup):
    companies = []
    for jobs in page_soup.find_all(name="div", attrs={"class": "data-results-content-parent relative"}):
        for div in jobs.findAll('div', {'class': 'data-details'}):
            for span in div.select('.data-details > span:nth-of-type(1)'):
                companies.append(span.text)
    return (companies)
z=list(company(page_soup))

def weblink(page_soup):
    weblinks = []
    for jobs in page_soup.find_all(name="div", attrs={"class": "data-results-content-parent relative"}):
        links = jobs.find('a', {'class': 'data-results-content'}).get('href')
        website = 'https://www.careerbuilder.com'
        weblinks.append(website + str(links))

    return weblinks
a=list(weblink(page_soup))

def jobid(page_soup):
  nwlnk = []
  job_soup=[]
  for jobs in page_soup.find_all(name="div", attrs={"class": "data-results-content-parent relative"}):
    links = jobs.find('a', {'class': 'data-results-content'}).get('href')
    website = 'https://www.careerbuilder.com'
    nwlnk.append(website + str(links))
  for nwl in nwlnk:
    job_response = requests.get(nwl)
    job_data = job_response.text
    job_soup.append(soup(job_data, "html.parser"))

  jobids=[]
  for job in job_soup:
    p = job.find('p', {'class': 'seperate-bottom normal'})
    if p is None:
          jobids.append("nothing found")
    else:
          jobids.append(p.text)
  return jobids


j = list(jobid(page_soup))

m=[]
n=[]
o=[]
p=[]
q=[]
def pagination(page_soup):
    newwebsitelink = []
    link_soup=[]

    urlpage = page_soup.find_all(name='div', attrs= {'id':'load_more_jobs'})

    if urlpage != []:
           url_tag = page_soup.find('a', {'class': 'btn btn-clear btn-clear-blue b-i'}).get('href')
           new_website = 'https://www.careerbuilder.com'

           newwebsitelink.append(new_website + str(url_tag))
           print(newwebsitelink)
           for nwsl in newwebsitelink:
                 link_response = requests.get(nwsl)
                 link_data = link_response.text
                 link_soup.append(soup(link_data, "html.parser"))
                 for newdata in link_soup:
                     m.append(position(newdata))
                     n.append(location(newdata))
                     o.append(company(newdata))
                     p.append(weblink(newdata))
                     q.append(jobid(newdata))
                     if newdata is not None:

                        pagination(newdata)
                     else:
                        break

    return m,n,o,p,q


t = pagination(page_soup)
print(t)

loc=[]
pos=[]
com=[]
webl=[]
jid=[]

loc=reduce(lambda x,y:x+y,t[0])
pos=reduce(lambda x,y:x+y,t[1])
com=reduce(lambda x,y:x+y,t[2])
webl=reduce(lambda x,y:x+y,t[3])
jid=reduce(lambda x,y:x+y,t[4])

zippedList = list(zip(x+loc,y+pos,z+com,a+webl,j+jid))
dfObj=pd.DataFrame(zippedList,columns=['position','location','Company','link','Jobid'])
s=pd.DataFrame(dfObj).to_csv('outputcareerbuild1.csv',header=True,index=None)
print(s)



