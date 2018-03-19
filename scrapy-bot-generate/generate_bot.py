#! /usr/bin/python

import json
from shutil import copyfile
import urllib

#json_file='a.json' 
json_file='zeroday.spider'

json_data=open(json_file)
data = json.load(json_data)
json_data.close()

newbot = data['bot_name']+".py"

copyfile('template.py', newbot)

# OPEN TEMPLATE FILE
f = open(newbot,'r')
filedata = f.read()
f.close()
# DECODE URLS
login_url = urllib.unquote(data['login_url']).decode('utf8') 
forum_url = urllib.unquote(data['forum_url']).decode('utf8') 

# REPLACE TEMPLATE CONTENTS
newdata = filedata.replace('name = "XXX"',"name = '"+data['bot_name']+"'")
newdata = newdata.replace("xxxSpider",data['bot_name']+"Spider")
newdata = newdata.replace("start_urls = ['XXX']","start_urls = ['"+login_url+"']")
newdata = newdata.replace('forum_url = "XXX"',"forum_url ='"+forum_url+"'")
newdata = newdata.replace("subforums = 'XXX'","subforums = '"+data['subforums_selector']+"'")
newdata = newdata.replace("threads = 'XXX'","threads = '"+data['threads_list']+"'")
newdata = newdata.replace("titles = 'XXX'","titles = '"+data['threads_titles']+"'")
newdata = newdata.replace("pagtitle = 'XXX'","pagtitle = '"+data['page_title']+"'")
newdata = newdata.replace("postdate = 'XXX'","postdate = '"+data['post_date']+"'")
newdata = newdata.replace("threadpages='XXX'","threadpages='"+data['thread_pages']+"'")
newdata = newdata.replace("username = 'XXX'","username ='"+data['login_user']+"'")
newdata = newdata.replace("password = 'XXX'","password = '"+data['login_password']+"'")
# DUMP NEW CONTENT
f = open(newbot,'w')
f.write(newdata)
f.close()
