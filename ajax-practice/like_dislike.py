#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import json
import jinja2
import logging
from google.appengine.ext import ndb
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir), autoescape=True)

class Post(ndb.Model) :
	content = ndb.StringProperty(required = True)
	likes = ndb.IntegerProperty(default = 0)
	dislikes = ndb.IntegerProperty(default = 0)

class Handler(webapp2.RequestHandler) :
	def write(self, *a, **kw) :
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params) :
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw) :

		self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
    	post = Post.get_or_insert("id", content = "THE AJAX CONQUER")
    	self.render("like_dislike.html", post = post)

    def post(self) :
    	# we have to put this for returning json
        self.response.headers = {'Content-Type': 'application/json; charset=utf-8'}
    	# load json from request
        data = json.loads(self.request.body)
        post = ndb.Key(Post, data['post']).get()
        if data["option"] == "like" :
            post.likes = post.likes + 1
        else :
            post.dislikes = post.dislikes + 1
        post.put()
        self.response.out.write(json.dumps(({'post': post.to_dict()})))

    	# self.write(json.dumps({'post' : post.to_dict()}))
    

app = webapp2.WSGIApplication([
    ('/ajax', MainHandler)
], debug=True)
