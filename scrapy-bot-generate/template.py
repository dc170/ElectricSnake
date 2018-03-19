import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import FormRequest
import hashlib
import pymongo
from pymongo import MongoClient


class xxxSpider(scrapy.Spider):
	# BOT NAME
	name = "XXX"
	# LOGIN URL
	start_urls = ['XXX']
	# MAIN URL
	forum_url = "XXX"
	# LIST OF SUBFORUMS
	subforums = 'XXX'
	# LIST OF THREADS IN SUBFORUM
	threads = 'XXX'
	# LIST OF THREAD'TITLES IN SUBFORUM
	titles = 'XXX'
	# PAGE TITLE
	pagtitle = 'XXX'
	# THREAD DATE
	postdate = 'XXX'
	# THREAD PAGES
	threadpages='XXX'
	# USER
	username = 'XXX'
	password = 'XXX'
	# BEGIN MONGO DB SETTINGS
	client = MongoClient()
	client = MongoClient('localhost', 27017)
	db = client['tor1']
	# END MONGO DB SETTINGS
	
	def parse(self, response):
		return [FormRequest.from_response(response,
			formdata={'username': username, 'password': password,
			callback=self.after_login)]

	def after_login(self, response):
		url = "http://qzbkwswfv5k2oj5d.onion/"
		subforums = response.xpath(self.subforums).extract()
		for forum in subforums:
			sf = self.forum_url+forum
			
			yield scrapy.Request(url=sf, callback=self.scan_subforum)
	def scan_subforum(self, response):
		threads = response.xpath(self.threads).extract()
		titles = response.xpath(self.titles).extract()
		number_of_posts = len(titles)
		subforum = response.xpath(self.pagtitle).extract()[0]
		
		for i in xrange(len(titles)):
			nurl = self.forum_url+threads[i]


			yield scrapy.Request(url=nurl, callback=self.inspect_post,  meta={'subforum':subforum,'title': titles[i], 'url':nurl})
	def inspect_post(self, response):
		title = response.meta.get('title')
		url = response.meta.get('url')
		date = response.xpath(self.postdate).extract()[0]
		pages = response.xpath(self.threadpages).extract()

		counter = 0

		for p in pages:
			counter +=1
			yield scrapy.Request(url=self.forum_url+p, callback=self.dump_html,  meta={'date':date,'subforum':response.meta.get('subforum'),'title': title, 'url':url, 'counter':counter})
	def dump_html(self, response):
		subforum = response.meta.get('subforum')
		title = response.meta.get('title')
		mainurl = response.meta.get('url')
		url = response.request.url
		date = response.meta.get('date')
		pagnum = response.meta.get('counter')
		print("SUBFORUM: "+subforum)
		print("POST TITLE: "+title)
		print("MAIN URL: "+mainurl)
		print("PAG URL["+str(pagnum)+"]: "+url)
		m = hashlib.md5()

		html = response.body
		identifier = hashlib.md5(html).hexdigest()
		print("MD5 HASH OF THE CONTENT: "+identifier)
		print("---------------------------")
		
		
		forumkey = {'pag_url':url}
		forumdata = {'date':date,'subforum':subforum, 'post_title':title, 'post_url':mainurl, 'pag_num':str(pagnum), 'content_hash':identifier, 'html':html}

		subforums = self.db.zerodayforum
		
		subforums.update_one(forumkey, {'$set':forumdata}, upsert=True)

