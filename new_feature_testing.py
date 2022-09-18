#%%
#BloombergQuint

from bs4 import BeautifulSoup
import requests
import csv
import time
from datetime import datetime
import pandas as pd
p = 5
count = 0
marketwatch = []
url = 'https://www.bqprime.com/markets?query=read-more'
r = requests.get(url) 
web_c = BeautifulSoup(r.text,'lxml')
web_c = web_c.findAll('h3',class_='topic-page__item__headline')
# web_c = web_c.find('li')
for i in web_c:
  k = i.find('a')
  # print(k.text,"https://www.bqprime.com" +k['href'])
  source = "https://www.bqprime.com" +k['href']
  marketwatch.append([k.text,source])


bq = pd.DataFrame(marketwatch, columns = ['News','Link'])
bq = bq.drop_duplicates(subset=["News"], keep='first')
bq.dropna(subset=['News'], inplace=True)
bq.to_csv('bloombergquint.csv')
bq
                                              
#%%
#EconomicTimes

from bs4 import BeautifulSoup
import requests
import csv
import time
from datetime import datetime
import pandas as pd
p = 5
count = 0
marketwatch = []
url = 'https://economictimes.indiatimes.com/markets'
r = requests.get(url) 
web_c = BeautifulSoup(r.text,'lxml')
web_c = web_c.findAll('a',class_='font_faus')
# web_c = web_c.find('li')
len(web_c)
for i in web_c:
  # k = i.find('li')
  source = "https://economictimes.indiatimes.com/" + i['href']
  marketwatch.append([i.text,source])


et = pd.DataFrame(marketwatch, columns = ['News','Link'])
et = et.drop_duplicates(subset=["News"], keep='first')
et.dropna(subset=['News'], inplace=True)
et.to_csv('economictimes.csv')
et

#%%                                     
#MoneyControl

from bs4 import BeautifulSoup
import requests
import csv
import time
from datetime import datetime
import pandas as pd
p = 5
count = 0
marketwatch = []
url = 'https://www.moneycontrol.com/news/business/markets/'
r = requests.get(url) 
web_c = BeautifulSoup(r.text,'lxml')
web_c = web_c.findAll('li',class_='clearfix')
for i in web_c:
  p = i.find('a',href = True)
  # print(p['href'])
  k = i.find('h2')
  # print(p['href'])
  k1 = str(k)
  if str(k) != 'None':
    news = k1.split('>')[2].replace('</a','').replace('</span','')
    # print(news,p['href'])
    marketwatch.append([news,p['href']])


mc = pd.DataFrame(marketwatch, columns = ['News','Link'])
mc = mc.drop_duplicates(subset=["News"], keep='first')
mc.dropna(subset=['News'], inplace=True)
mc.to_csv('MoneyControl.csv')  
                                              
#MarketWatch

from bs4 import BeautifulSoup
import requests
import csv
import time
from datetime import datetime
import pandas as pd
p = 5
count = 0
marketwatch = []
while count != p:
  url = 'https://www.marketwatch.com/latest-news?mod=top_nav'
  r = requests.get(url) 
  web_c = BeautifulSoup(r.text,'lxml')
  web_c = web_c.findAll('div',class_='article__content')
  
  for i in web_c:
    k = i.findAll('a',class_='link')
    for i in k:
      marketwatch.append([i.text,i['href']])
  df = pd.DataFrame(marketwatch, columns = ['News','Link'])
  df = df.drop_duplicates(subset=["News"], keep='first')
  df.dropna(subset=['News'], inplace=True)
  df.to_csv('file1.csv')  
  count += 1                                              
  time.sleep(1)


df

#%%
#MMI
@app.route('/mmi') 
def mmi():
    URL = 'https://www.tickertape.in/market-mood-index'
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
                'Accept-Language': 'en-US, en;q=0.5'})
  
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    mmi = dom.xpath('//*[@id="app-container"]/div/div[1]/div[1]/div/div[2]/span')[0].text
    day = dom.xpath('//*[@id="app-container"]/div/div[1]/div[1]/div/div[2]/p/text()[2]')[0]
    return render_template("MMI.html",mmi_page = mmi,last_updated = day)

# MF Bhav Sheet https://www.amfiindia.com/nav-history-download

def mffull():
    k = 'https://www.amfiindia.com/spages/NAVAll.txt'
    response = requests.get(k)
    df = pd.DataFrame( columns=['Scheme Code','ISIN Div Payout/ ISIN Growth','ISIN Div Reinvestment','Scheme Name','Net Asset Value','Date'])
    data = response.text.split("\n")
    for scheme_data in data:
        if ";INF" in scheme_data:
            scheme = scheme_data.split(";")
            scheme[5] = scheme[5].replace('\r','')
            if 'Aug-2022' in scheme[5]:
                df.loc[len(df)] = scheme
    return df

@app.route('/mffull/api') 
def mffullapi():
    df = mffull()
    return Response(df.to_json(), mimetype='application/json')

@app.route('/mffull')
def mffullapi():
    df = mffull()
    return render_template('view.html',tables=[df.to_html()])

#%%
def mffull():
    k = 'https://www.amfiindia.com/spages/NAVAll.txt'
    response = requests.get(k)
    df = pd.DataFrame( columns=['Scheme Code','ISIN Div Payout/ ISIN Growth','ISIN Div Reinvestment','Scheme Name','Net Asset Value','Date'])
    data = response.text.split("\n")
    for scheme_data in data:
        if ";INF" in scheme_data:
            scheme = scheme_data.split(";")
            scheme[5] = scheme[5].replace('\r','')
            if 'Aug-2022' in scheme[5]:
                df.loc[len(df)] = scheme
    return df

@app.route('/mf')
def mf():
    df = mffull()
    return render_template('view.html',tables=[df.to_html()])
    