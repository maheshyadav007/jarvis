# -*- coding:utf8 -*-
#!/usr/bin/env python 
# Copyright 2017 Google Inc. All Rights Reserved.
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

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)

	print("Request:")
	print(json.dumps(req, indent=4))

	res = processRequest(req)

	res = json.dumps(res, indent=4)
	# print(res)
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r


def processRequest(req):
	if req.get("result").get("action") != "news.search":
		return {}
	baseurl = "https://newsapi.org/v2/top-headlines?"#https://query.yahooapis.com/v1/public/yql?"
	yql_query = makeYqlQuery(req)
	#print (yql_query)
	if yql_query is None:
		return {}
	yql_url = baseurl + urlencode({'q': yql_query})# + "&format=json"
	result = urlopen(yql_url).read()
	data = json.loads(result)
	res = makeWebhookResult(data)
	return res


def makeYqlQuery(req):
	result = req.get("result")
	parameters = result.get("parameters")
	q = parameters.get("keyword")
	datetime=parameters.get("date-time")
	category=parameters.get("category")
	source=parameters.get("source")
	sort=parameters.get("sort")
	
##	if q is None:
##		return None
##	if datetime is None:
##		return None
##	if category is None:
##		return None
##	if sources is None:
##		return None
##	if sort is None:
##		return None


	

	return "sources="+bbc-news+"&apiKey=e15bb246cdc445f1ab7761ad4e0b4599"#"q="+q+"&date-time="+datetime+"&category="+category+"sources="+sources+"&sort="+sort+"&apiKey=e15bb246cdc445f1ab7761ad4e0b4599"#select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"
		

def makeWebhookResult(data):
##	articles = data[articles]
##	if articles is None:
##		return {}
##
##	desc= articles[0]
##	if desc is None:
##		return {}
##	description=desc['description']
##	if description is None:
##		return{}

##    channel = result.get('channel')
##    if channel is None:
##        return {}
##
##    item = channel.get('item')
##    location = channel.get('location')
##    units = channel.get('units')
##    if (location is None) or (item is None) or (units is None):
##        return {}
##
##    condition = item.get('condition')
##    if condition is None:
##        return {}

	# print(json.dumps(item, indent=4))

	speech = "Here is the news headlines: "#+description

	print("Response:")
	print(speech)

	return {
		"speech": speech,
                "source": "webhook",
		"displayText":speech}
		#"data":{
		#},
		#"contextOut": [],
		
	


if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))

	print("Starting app on port %d" % port)

	app.run(debug=False, port=port, host='0.0.0.0')
