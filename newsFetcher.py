import os
import requests
import time
from datetime import datetime
import dateutil.parser
import pprint
import feedparser

from bs4 import BeautifulSoup
from models import db
from article import Article

pp = pprint.PrettyPrinter(indent=4)


#Request HTML data from link and parse it with BeautifulSoup
def returnCoolHTML(url):
    heads = {'Accept-Language':'en-US','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Connection':'keep-alive','Referer':'216.58.220.196'}
    while (True):
        try:
            req=requests.get(url,headers=heads)
        except requests.exceptions.ConnectionError as e:
            print("Conncetion Error. Trying again.")
            time.sleep(1.2)
            continue
        break
    data=BeautifulSoup(req.text,"html5lib")
    req.close()
    return data

#Request XML data from link and parse it with BeautifulSoup
def returnCoolXML(url):
    heads = {'Accept-Language':'en-US','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Connection':'keep-alive','Referer':'216.58.220.196'}
    while (True):
        try:
            req=requests.get(url,headers=heads)
        except requests.exceptions.ConnectionError as e:
            print("Conncetion Error. Trying again.")
            time.sleep(1.2)
            continue
        break
    time.sleep(0.5)
    data=BeautifulSoup(req.text,"xml")
    req.close()
    time.sleep(0.4)
    return data

#Fetch articles from BBC News
def getBBCArticle():
	data = returnCoolHTML('http://feeds.bbci.co.uk/news/politics/rss.xml')

	for article in data.find_all("item"):
		url = article.find("guid").get_text()
		print(url)
		if not db['_article'].find({'url':url}).count():
			a = Article(article.find("guid").get_text())
			page = returnCoolHTML(article.find("guid").get_text())
			if page.find(class_="story-body__inner"):
				body = ""
				for paragraph in page.find(class_="story-body__inner").find_all("p"):
					body += paragraph.get_text().strip() + " "
				a.body = body
			if page.find(class_="vxp-media__summary"):
				body = ""
				for paragraph in page.find(class_="vxp-media__summary").find_all("p"):
					body += paragraph.get_text().strip() + " "
				a.body = body
			if page.find('h1'):
				a.title = page.find('h1').get_text()
			if page.find('div', {"class": "date"}):
				a.datePublished = datetime.fromtimestamp(float(page.find('div', {"class": "date"})["data-seconds"]))
			if page.find('li', {"class":"mini-info-list__item"}) and page.find('li', {"class":"mini-info-list__item"}) and  page.find('li', {"class":"mini-info-list__item"}).find('div').has_attr('data-seconds'):
				a.datePublished = datetime.fromtimestamp(float(page.find('li', {"class":"mini-info-list__item"}).find('div')['data-seconds']))
			a.source = "BBC"
			out = db['_article'].insert_one(a.__dict__)
			print('Inserted 1 article in db\n')

#Fetch articles from The Guardian
def getGuardianNews():
	data = returnCoolXML('https://www.theguardian.com/politics/rss')
	count = 0
	for article in data.find_all("item"):
		url = article.find("link").get_text()
		print(url)
		if not db['_article'].find({'url':url}).count():
			a = Article(article.find("link").get_text())
			page = returnCoolHTML(article.find("link").get_text())
			if page.find('time') and page.find('time').has_attr('data-timestamp'):
				a.datePublished = datetime.fromtimestamp(float(page.find('time')['data-timestamp'][0:10]))
				# print(a.datePublished)
			if page.find(class_="content__headline"):
				a.title = page.find(class_="content__headline").get_text().strip()
			if page.find(class_="content__article-body"):
				body = ""
				for paragraph in page.find(class_="content__article-body").find_all('p'):
					body += paragraph.get_text().strip() + " "
				a.body = body
			a.source = "The Guardian"
			out = db['_article'].insert_one(a.__dict__)
			print('Inserted 1 article in db\n')

#Fetch articles from Sky News
def getSkyNews():
	data = returnCoolXML('http://feeds.skynews.com/feeds/rss/politics')
	for article in data.find_all("item"):
		url = article.find("link").get_text()
		print(url)
		if not db['_article'].find({'url':url}).count():
			a = Article(article.find("link").get_text())
			page = returnCoolHTML(article.find("link").get_text())
			if page.find(class_="sdc-news-article-header__last-updated__timestamp"):
				a.datePublished = print(dateutil.parser.parse(page.find(class_="sdc-news-article-header__last-updated__timestamp")['datetime']))
				# print(a.datePublished)
			if page.find(class_="sdc-news-article-header__headline "):
				a.title = page.find(class_="sdc-news-article-header__headline ")['aria-label']#.get_text().strip()
				# print(a.title)
			body = ""
			if page.find(class_="sdc-news-story-article__intro"):
				body += page.find(class_="sdc-news-story-article__intro").get_text().strip() + " "
			if page.find(class_="sdc-news-story-article__body"):
				for paragraph in page.find(class_="sdc-news-story-article__body").find_all('p'):
					body += paragraph.get_text().strip() + " "
				a.body = body
			a.source = "Sky News"
			out = db['_article'].insert_one(a.__dict__)
			print('Inserted 1 article in db\n')

#Fetch articles from The Independent
def getIndependentNews():
	data = returnCoolXML('http://www.independent.co.uk/news/uk/politics/rss')
	for article in data.find_all("item"):
		url = article.find("link").get_text()
		print(url)
		if not db['_article'].find({'url':url}).count():
			a = Article(article.find("link").get_text())
			page = returnCoolHTML(article.find("link").get_text())
			if page.find('time') and page.find('time').has_attr('data-microtimes'):
				a.datePublished = datetime.fromtimestamp(float(eval(page.find('time')['data-microtimes'])['published'][0:10]))
				# print(a.datePublished)
			if page.find('h1'):
				a.title = page.find('h1').get_text().strip()
				# print(a.title)
			if page.find(class_="text-wrapper"):
				body = ""
				for paragraph in page.find(class_="text-wrapper").find_all('p'):
					if paragraph.parent.name == "div":
						body += paragraph.get_text().strip() + " "
				a.body = body
			a.source = "The Independent"
			out = db['_article'].insert_one(a.__dict__)
			print('Inserted 1 article in db\n')

#Fetch articles from all four sources one by one
def fetchAll():
	getBBCArticle()
	getGuardianNews()
	getSkyNews()
	getIndependentNews()

#One time fetching for US Election from BBC News
def fetchUSElectionBBC():
	for i in range(1,3):
		print("==========================")
		print(i)
		data = returnCoolHTML("https://www.bbc.co.uk/search?q=us+election&sa_f=search-product&filter=news&suggid=#page="+str(i))
		for headline in data.find_all("h1"):
			print(headline.find("a")["href"])
		print(data.find(class_="pagination"))

#One time fetching for US Election from The Independent
def fetchUSElectionIndependent():
	for i in range(280,631):
		print("==========================")
		print(i)
		data = returnCoolHTML("https://www.independent.co.uk/search/site/us%2520election?page="+str(i))
		for headline in data.find_all("h2"):
			if headline.find("a"):
				url = headline.find("a")["href"]
				print(url)
				if not db['_past_article'].find({'url':url}).count():
					a = Article(url)
					page = returnCoolHTML(url)
					if page.find('time') and page.find('time').has_attr('data-microtimes'):
						a.datePublished = datetime.fromtimestamp(float(eval(page.find('time')['data-microtimes'])['published'][0:10]))
						print(a.datePublished)
					if page.find('h1') and len(str(page.find('h1'))) <= 200:#, {"class":"headline article-width"}):
						a.title = page.find('h1').get_text().strip()
						print(a.title)
					if page.find(class_="text-wrapper"):
						body = ""
						for paragraph in page.find(class_="text-wrapper").find_all('p'):
							if paragraph.parent.name == "div":
								body += paragraph.get_text().strip() + " "
						a.body = body
					a.source = "The Independent"
					out = db['_past_article'].insert_one(a.__dict__)
					print(out)

#One time fetching for US Election from Sky News
def fetchUSElectionSkyNews():
	for i in range(1,51):
		print("==========================")
		print(i)
		data = returnCoolHTML("https://news.sky.com/search?q=us+election&sortby=date&page="+str(i))
		for headline in data.find_all("h2"):
			if headline.find("a"):
				url = headline.find("a")["href"]
				print(url)
				if not db2['_past_article'].find({'url':url}).count():
					a = Article(url)
					page = returnCoolHTML(url)
					if page.find(class_="sdc-news-article-header__last-updated__timestamp"):
						a.datePublished = dateutil.parser.parse(page.find(class_="sdc-news-article-header__last-updated__timestamp")['datetime'])
						print("date", a.datePublished)
					if page.find(class_="sdc-news-article-header__headline "):
						a.title = page.find(class_="sdc-news-article-header__headline ").find("span").get_text()#['aria-label']#.get_text().strip()
						print("title", a.title)
					body = ""
					if page.find(class_="sdc-news-story-article__intro"):
						body += page.find(class_="sdc-news-story-article__intro").get_text().strip() + " "
					if page.find(class_="sdc-news-story-article__body"):
						for paragraph in page.find(class_="sdc-news-story-article__body").find_all('p'):
							body += paragraph.get_text().strip() + " "
						a.body = body
					a.source = "Sky News"
					out = db2['_past_article'].insert_one(a.__dict__)
					print(out)
