# Copyright 2016 Google Inc.
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

import webapp2
import jinja2
import os
import re

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class mainpage(webapp2.RequestHandler):
    def valid(self, value, para):
        username = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        password = re.compile(r"^.{3,20}$")
        email = re.compile("^[\S]+@[\S]+.[\S]+$")
        
        if para == 'username':
            return username.match(value)
        elif para == 'password':
            return password.match(value)
        elif para == 'email':
            return email.match(value)
 
    def get(self):
        template_values = {
            'username': "",
            'password': "",
            'verify': "",
            'email': "",
            'usernameER': "",
            'passwordER': "",
            'verifyER': "",
            'emailER': ""
        }
        
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        
        u = "That's not a valid username."
        p = "That wasn't a valid password."
        v = "Your passwords didn't match."
        e = "That's not a valid email."
        
        if self.valid(username, 'username'):
            u = ""
        if self.valid(password, 'password'):
            p = ""
            if password == verify:
              v = ""
        if email == "" or self.valid(email, 'email'):
            e = ""
        
        if not u and not p and not v and not e:
            self.redirect("/welcome?q=" + username)
        else:
            password = ""
            verify = ""
            if p:
                v = ""
        
            template_values = {
                'username': username,
                'password': password,
                'verify': verify,
                'email': email,
                'usernameER': u,
                'passwordER': p,
                'verifyER': v,
                'emailER': e
            }

            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render(template_values))

class welcomepage(webapp2.RequestHandler):
    def get(self):
        q = self.request.get('q')
        self.response.write("Welcome " + q + "!")


app = webapp2.WSGIApplication([
    ('/', mainpage),('/welcome', welcomepage)
], debug=True)
