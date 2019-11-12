#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'export_to_telegraph'
token = ''

import requests
from bs4 import BeautifulSoup
from html_telegraph_poster import TelegraphPoster
import traceback as tb

class _Article(object):
	def __init__(self, title, author, text):
		self.title = title
		self.author = author
		self.text = text

def _getPoster():
	global token
	if token:
		return TelegraphPoster(access_token = token)
	p = TelegraphPoster()
	r = p.create_api_token('export_to_telegraph', 'export_to_telegraph')
	token = r['access_token']
	return p

def _wechat2Article(soup):
	title = soup.find("h2").text.strip()
	author = soup.find("a", {"id" : "js_name"}).text.strip()
	g = soup.find("div", {"id" : "js_content"})
	for img in g.find_all("img"):
		b = soup.new_tag("figure")
		b.append(soup.new_tag("img", src = img["data-src"]))
		img.append(b)
	for section in g.find_all("section"):
		b = soup.new_tag("p")
		b.append(BeautifulSoup(str(section), features="lxml"))
		section.replace_with(b)
	return _Article(title, author, g)
	

def _stackoverflow2Article(soup):
	title = soup.find("title").text.strip()
	title = title.replace('- Stack Overflow', '').strip()
	g = soup.find("div", class_ = "answercell")
	g = g.find("div", class_ = "post-text")
	for section in g.find_all("section"):
		b = soup.new_tag("p")
		b.append(BeautifulSoup(str(section), features="lxml"))
		section.replace_with(b)
	
	return _Article(title, 'Stack Overflow', g)

def _bbc2Article(soup):
	title = soup.find("h1").text.strip()
	g = soup.find("div", class_ = "story-body__inner")
	for elm in g.find_all('span', class_="off-screen"):
		elm.decompose()
	for elm in g.find_all('ul', class_="story-body__unordered-list"):
		elm.decompose()
	for elm in g.find_all('span', class_="story-image-copyright"):
		elm.decompose()
	for img in g.find_all("div", class_="js-delayed-image-load"):
		b = soup.new_tag("figure", width=img['data-width'], height=img['data-height'])
		b.append(soup.new_tag("img", src = img["data-src"], width=img['data-width'], height=img['data-height']))
		img.replace_with(b)
	for section in g.find_all("section"):
		b = soup.new_tag("p")
		b.append(BeautifulSoup(str(section), features="lxml"))
		section.replace_with(b)
	return _Article(title, 'BBC', g)

_NYT_ADS = '《纽约时报》推出每日中文简报'
_ADS_SUFFIX = '订阅《纽约时报》中文简报'
ADS_WORDS = set(['The Times is committed', 'Follow The New York Times'])

def _nyt2Article(soup):
	title = soup.find("meta", {"property": "twitter:title"})['content'].strip()
	author = soup.find("meta", {"name": "byl"})['content'].strip()
	g = soup.find("article")
	for link in g.find_all("a"):
		if not '英文版' in link.text:
			link.replace_with(link.text)
	for item in g.find_all("div", class_="article-header"):
		item.decompose()
	for item in g.find_all("small"):
		item.decompose()
	for item in g.find_all("header"):
		item.decompose()
	for item in g.find_all("div", {"id":"top-wrapper"}):
		item.decompose()
	for item in g.find_all("div", class_="bottom-of-article"):
		item.decompose()
	for item in g.find_all("div", {"id":"bottom-wrapper"}):
		item.decompose()
	for item in g.find_all("div", class_="article-paragraph"):
		if item.text and (_NYT_ADS in item.text or _ADS_SUFFIX in item.text):
			item.decompose()
		elif item.text == '广告':
			item.decompose()
		else:
			wrapper = soup.new_tag("p")
			wrapper.append(BeautifulSoup(str(item), features="lxml"))
			item.replace_with(wrapper)
	for item in g.find_all("p"):
		for word in ADS_WORDS:
			if word in item.text:
				item.decompose()
				continue
	for item in g.find_all("footer", class_="author-info"):
		for subitem in item.find_all("a"):
			if subitem.text and "英文版" in subitem.text:
				item.replace_with(subitem)
				break
	return _Article(title, author + ' - NYT', g)

def _telegraph2Article(soup):
	title = soup.find("meta", {"name": "twitter:title"})['content'].strip()
	author = soup.find("meta", {"property": "article:author"})['content'].strip()
	g = soup.find("article")
	item = g.find('h1')
	if item:
		item.decompose()
	item = g.find('address')
	if item:
		item.decompose()
	return _Article(title, author, g)

def _getArticle(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	if "mp.weixin.qq.com" in url:
		return _wechat2Article(soup)
	if "stackoverflow.com" in url:
		return _stackoverflow2Article(soup)
	if "bbc.com" in url:
		return _bbc2Article(soup)
	if "bbc.in" in url:
		return _bbc2Article(soup)
	if "nytimes.com" in url:
		return _nyt2Article(soup)
	if "telegra.ph" in url:
		return _telegraph2Article(soup)
	if "nyt" in url:
		return _nyt2Article(soup)
	return _telegraph2Article(soup)

def _trimUrl(url):
	if not '://' in url:
		return url
	loc = url.find('://')
	return url[loc + 3:]

def _formaturl(url):
	if '://' not in url:
		return "https://" + url
	return url

def export(url, throw_exception=False):
	try:
		p = _getPoster()
		article = _getArticle(_formaturl(url))
		r = p.post(
			title = article.title, 
			author = article.author, 
			author_url = _formaturl(url), 
			text = str(article.text)[:80000])
		return _trimUrl(r['url'])
	except Exception as e:
		if throw_exception:
			raise e

def _test():
	url = 'https://www.nytimes.com/2019/10/10/opinion/sunday/feminism-lean-in.html'
	article = _getArticle(_formaturl(url))
	with open('tmp.html','w') as f:
		f.write(str(article.text))
	return export(url)

_test()



