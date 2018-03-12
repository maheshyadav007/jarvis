
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import requests
import json






def webhook():
	#req = request.get_json(silent=True, force=True)
##
##	print("Request:")
##	print(json.dumps(req, indent=4))
	print ("my")
	res = processRequest(",njcdkc")
	print("my")
	res = json.dumps(res, indent=4)
	print ("my")
	# print(res)
	#r = make_response(res)
	#r.headers['Content-Type'] = 'application/json'
	return res


def processRequest(req):
	
	baseurl = "https://newsapi.org/v2/top-headlines?"#https://query.yahooapis.com/v1/public/yql?"
	yql_query = makeYqlQuery(req)
	
	
	yql_url = baseurl + yql_query#urlencode({'q': yql_query})#+ "&format=json"
	print (yql_url)
	headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format("e15bb246cdc445f1ab7761ad4e0b4599")}
	
	result = requests.get(yql_url,headers=headers).content.decode('utf-8')
	print("result")
	data = json.loads(result)
	print(data)
	res = makeWebhookResult(data)
	return res


def makeYqlQuery(req):
##	result = req.get("result")
##	parameters = result.get("parameters")
##	q = parameters.get("keyword")
##	datetime=parameters.get("date-time")
##	category=parameters.get("category")
##	source=parameters.get("source")
##	sort=parameters.get("sort")
##	
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


	

	return "sources="+"bbc-news"#"q="+q+"&date-time="+datetime+"&category="+category+"sources="+"bbc-news"+"&sort="+sort+"&apiKey=e15bb246cdc445f1ab7761ad4e0b4599"#select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"
		

def makeWebhookResult(data):
##	article = data.get('articles')
##	if article is None:
##		return {}
##
##	desc= article[0]
##	if desc is None:
##		return {}
##	description=desc.get('description')
##	if description is None:
##		return{}
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

##	speech = "Here is the news headlines:;lkofsdofjsfjsfjisfsef "+description
	
	speech = "News headlines: "+description1+" "+description2+" "+description3
	print("Response:")
	print(speech)

	return {
		"speech": speech,
		"source": "webhook",
		"displayText":speech}
		#"data":{
		#},
		#"contextOut": [],
webhook()
