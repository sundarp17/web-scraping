import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
from urllib.request import urlopen as ureq
from functools import reduce

my_url="https://citeseerx.ist.psu.edu/search?q=natural+language+processing&t=doc&sort=rlv&start=0"
uclient = ureq(my_url)
page_html = uclient.read()
uclient.close()
page_soup = soup(page_html, "html.parser")

def abstract(page_soup):
    weblinks=[]
    new_soup=[]
    for div in page_soup.find_all(name="div",attrs={"class": "result"}):
        links = div.find('a', {'class': 'remove doc_details'}).get('href')
        website="https://citeseerx.ist.psu.edu"
        weblinks.append(website + str(links))
    for nwl in weblinks:
        response = requests.get(nwl)
        data = response.text
        new_soup.append(soup(data, "html.parser"))
    abstracts=[]
    for abs in new_soup:
        id = abs.find('div', {'id': 'abstract'})
        for p in id.select('#abstract > p:nth-of-type(1)'):
            abstracts.append(p.text)
    return abstracts


x=list(abstract(page_soup))
print(len(x))

m=[]
def nextpage(page_soup):
    a=[10,20,30,40,50,60,70,80,90,100]
    for i in a:
        newurl="https://citeseerx.ist.psu.edu/search?q=natural+language+processing&t=doc&sort=rlv&start=" + str(i)
        response=requests.get(newurl)
        data=response.text
        newsoup=soup(data,'html.parser')
        m.append(abstract(newsoup))

    return m

y=list(nextpage(page_soup))
print(y[0])

zippedList = list(zip(x+y[0]+y[1]+y[2]+y[3]+y[4]+y[5]+y[6]+y[7]+y[8]))
dfObj=pd.DataFrame(zippedList,columns=['Abstract'])
s=pd.DataFrame(dfObj).to_csv('abstract.csv',header=True,index=None)
print(s)


