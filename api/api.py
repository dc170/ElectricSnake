from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
import json
from pymongo import MongoClient
from bson.json_util import dumps
from flask import request


db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)

client = MongoClient("localhost", 27017, maxPoolSize=50)

db = client.tor1
collection = db['zerodayforum']
    

class Posts(Resource):
    def get(self):
		cursor = collection.find({},{'date':1,'subforum':1, 'post_title':1, 'post_url':1, 'pag_num':1, 'content_hash':1, 'html':1,'_id': 0})
		array = list(cursor)
		json_string = json.dumps(array)
		resp = jsonify(array)
		return resp
		
class Posts_date(Resource):
    def get(self,date):
		cursor = collection.find({ 'date': date },{'date':1,'subforum':1, 'post_title':1, 'post_url':1, 'pag_num':1, 'content_hash':1, 'html':1,'_id': 0})
		array = list(cursor)
		json_string = json.dumps(array)
		resp = jsonify(array)
		return resp
#"username" : {$regex : ".*son.*"}
class Posts_html(Resource):
    def get(self):
		cursor = collection.find({ },{ 'html':1,'_id': 0})
		array = list(cursor)
		json_string = json.dumps(array)
		resp = jsonify(array)
		return resp
		
class Posts_contain_word(Resource):
    def get(self,word):
		cursor = collection.find({"html":{"$regex": u""+word+""}} ,{ 'date':1,'subforum':1, 'post_title':1, 'post_url':1, 'pag_num':1, 'content_hash':1, 'html':1,'_id': 0})
		array = list(cursor)
		json_string = json.dumps(array)
		resp = jsonify(array)
		return resp
		
		
class Posts_word_title(Resource):
    def get(self,word):
		cursor = collection.find({"post_title":{"$regex": u""+word+""}} ,{ 'date':1,'subforum':1, 'post_title':1, 'post_url':1, 'pag_num':1, 'content_hash':1, 'html':1,'_id': 0})
		array = list(cursor)
		json_string = json.dumps(array)
		resp = jsonify(array)
		return resp

class Posts_hash_content(Resource):
    def get(self,word):
		cursor = collection.find({"hash":{"$regex": u""+word+""}} ,{ 'date':1,'subforum':1, 'post_title':1, 'post_url':1, 'pag_num':1, 'content_hash':1, 'html':1,'_id': 0})
		array = list(cursor)
		json_string = json.dumps(array)
		resp = jsonify(array)
		return resp
#https://github.com/miguelgrinberg/REST-auth
class Posts_hash_title(Resource):
    def get(self,word):
		cursor = collection.find({"post_title":{"$regex": u""+word+""}} ,{ 'date':1,'subforum':1, 'post_title':1, 'post_url':1, 'pag_num':1, 'content_hash':1, 'html':1,'_id': 0})
		array = list(cursor)
		json_string = json.dumps(array)
		resp = jsonify(array)
		return resp


api.add_resource(Posts_hash_content, '/posts/hash/content/<word>') # 
api.add_resource(Posts_hash_title, '/posts/hash/title/<word>') # 
api.add_resource(Posts, '/posts') # 
api.add_resource(Posts_html, '/html') # 
api.add_resource(Posts_contain_word, '/html/<word>') # 
api.add_resource(Posts_word_title, '/posts/title/<word>') # 

api.add_resource(Posts_date, '/posts/date/<date>') # 


if __name__ == '__main__':
     app.run(port=5002)
