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
import os
import transit_graph as tg
import webapp2

from django.utils import simplejson
from google.appengine.ext.webapp import template

class MainHandler(webapp2.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.write(template.render(path, {}))

class RPCHandler(webapp2.RequestHandler):
  def get(self):
    distance_list = transit_graph.getShortestDistance(
        int(self.request.get('stopid')))
    results = [];
    for (stop_id, travel_time) in distance_list:
      results.append({"stop_id": stop_id, "seconds": travel_time})
    self.response.write(simplejson.dumps(results))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/rpc', RPCHandler)
], debug=True)

transit_graph = tg.TransitGraph(
    os.path.join(os.path.dirname(__file__),
    'transit_graph.csv'))
