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
	print("my")
	print(req)
	print(json.dumps(req, indent=4))
	print("req")
	res = processRequest(req)
	print(res)
	res = json.dumps(res, indent=4)
	
	#res="{"ffe":"edee"}"
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
	yql_url = baseurl + yql_query#urlencode({'q': yql_query})# + "&format=json"
##	result = urlopen(yql_url).read()
	print(yql_url)
	headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format("e15bb246cdc445f1ab7761ad4e0b4599")}
	
	result = requests.get(yql_url,headers=headers).content.decode('utf-8')
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
	
	if q & datetime & category & source & sort is None:
		return None
##	if datetime is None:
##		return None
##	if category is None:
##		return None
##	if sources is None:
##		return None
##	if sort is None:
##		return None


	

	return "q="+q+"&date-time="+datetime+"&category="+category+"&sources="+sources+"&sort="+sort#+"&apiKey=e15bb246cdc445f1ab7761ad4e0b4599"#select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"
		

def makeWebhookResult(data):
	article = data.get("articles")
	if article is None:
		return {}

	desc1= article[0]
	if desc1 is None:
		return {}
	description1=desc1['description']
	if description1 is None:
		return{}
	desc2= article[1]
	if desc2 is None:
		return {}
	description2=desc2['description']
	if description2 is None:
		return{}
	desc3= article[2]
	if desc3 is None:
		return {}
	description3=desc3['description']
	if description3 is None:
		return{}

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

	speech = "News headlines: "+description1+" "+description2+" "+description3

	print("Response:")
	print(speech)

	return {
		"speech": speech,
		"source": "newsai-webhook",
		"displayText":speech}
		#"data":{
		#},
		#"contextOut": [],
		
	


if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))

	print("Starting app on port %d" % port)

	app.run(debug=False, port=port, host='0.0.0.0')
