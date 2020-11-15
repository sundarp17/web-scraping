import requests
from bs4 import BeautifulSoup
import pandas as pd





def symbol(soup):
    symbols=[]
    for sym in soup.find_all(name="tr",attrs={"class":"simpTblRow"}):
        for symb in sym.find_all('td', attrs={'aria-label': 'Symbol'}):
            symbols.append(symb.text)
    return symbols
def name(soup):
    names=[]
    for i in soup.find_all(name="tr",attrs={"class":"simpTblRow"}):
        for j in i.find_all('td', attrs={'aria-label': 'Name'}):
            names.append(j.text)
    return names
def price(soup):
    prices=[]
    for i in soup.find_all(name="tr",attrs={"class":"simpTblRow"}):
        for j in i.find_all('td', attrs={'aria-label': 'Price (Intraday)'}):
            prices.append(j.text)
    return prices
def change(soup):
    changes=[]
    for i in soup.find_all(name="tr",attrs={"class":"simpTblRow"}):
        for j in i.find_all('td', attrs={'aria-label': 'Change'}):
            changes.append(j.text)
    return changes
def percent_change(soup):
    per_change=[]
    for i in soup.find_all(name="tr",attrs={"class":"simpTblRow"}):
        for j in i.find_all('td', attrs={'aria-label': '% Change'}):
            per_change.append(j.text)
    return per_change
def volume(soup):
    vol=[]
    for i in soup.find_all(name="tr",attrs={"class":"simpTblRow"}):
        for j in i.find_all('td', attrs={'aria-label': 'Volume'}):
            vol.append(j.text)
    return vol
def avg_vol_3months(soup):
    avg_vol=[]
    for i in soup.find_all(name="tr",attrs={"class":"simpTblRow"}):
        for j in i.find_all('td', attrs={'aria-label': 'Avg Vol (3 month)'}):
            avg_vol.append(j.text)
    return avg_vol
def market_cap(soup):
    market=[]
    for i in soup.find_all(name="tr",attrs={"class":"simpTblRow"}):
        for j in i.find_all('td', attrs={'aria-label': 'Market Cap'}):
            market.append(j.text)
    return market


urls=['https://finance.yahoo.com/most-active?offset=0&count=100','https://finance.yahoo.com/most-active?count=100&offset=100',
      'https://finance.yahoo.com/most-active?count=100&offset=200']

s=[]
n=[]
p=[]
c=[]
pc=[]
v=[]
av=[]
mc=[]

dfObj=pd.DataFrame(columns=['Symbol','Name','Price','Change','% Change','Volume','Avg Vol(3 months)','Market Cap'])
ex=pd.DataFrame(dfObj).to_csv('stocks.csv',header=True,index=None)
for i in urls:
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    r = requests.get(i, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    s=(symbol(soup))
    n=(name(soup))
    p=(price(soup))
    c=(change(soup))
    pc=(percent_change(soup))
    v=(volume(soup))
    av=(avg_vol_3months(soup))
    mc=(market_cap(soup))
    zippedList=list(zip(s,n,p,c,pc,v,av,mc))
    dfObj=pd.DataFrame(zippedList,columns=['Symbol','Name','Price','Change','% Change','Volume','Avg Vol(3 months)','Market Cap'])
    ex=pd.DataFrame(dfObj).to_csv('stocks.csv',header=False,index=None,mode='a')
print(ex)




