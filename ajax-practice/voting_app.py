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

class Story(ndb.Model) :
	title = ndb.StringProperty(required = True)
	vote_count = ndb.IntegerProperty(default = 0)

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
        story = Story.get_or_insert('some id or so', title = "A Voting Story Again")
        self.render("voting.html", story = story)
    def post(self) :
    	
    	data = json.loads(self.request.body)
    	story = ndb.Key(Story, data['storyKey']).get()
    	story.vote_count = story.vote_count + 1
    	story.put()
    	self.response.out.write(json.dumps(({'story': story.to_dict()})))

app = webapp2.WSGIApplication([
    ('/ajax', MainHandler)
], debug=True)
