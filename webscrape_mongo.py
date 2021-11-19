# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 17:57:50 2021

@author: Joe Silvan
"""


import requests
from bs4 import BeautifulSoup
from newspaper import Article
import pandas as pd
import nltk
nltk.download('punkt')
import pymongo

#Mongodb config
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["WebscrappingPOC"]
mycol = mydb["Scraped_data"]
# feed="http://abcnews.go.com/abcnews/technologyheadlines"
feed="https://abcnews.go.com/abcnews/businessheadlines"


#request and soup creation
response=requests.get(feed)
webpage=response.content
soup=BeautifulSoup(webpage,features='xml')
items=soup.find_all('item')


articles=[]
for item in items:
    link=item.find('link').text
    articles.append(link)
    
 
res=[]
for url in articles:
    article=Article(url)
    article.download()
    article.parse()
    article.nlp()
    
    
    title    =article.title
    summary  =article.summary
    keywords =article.keywords
    text     =article.text

    print("*******************")
    print(f"Title:{title}")
    print(f"URL:{url}")
    print(f"Keywords:{keywords}")
    print(f"summary:{summary}")
    print("****************")
    result={'Title':title,'URL':url,'Keywords':keywords,'summary':summary}
    res.append(result)
x = mycol.insert_many(res)
