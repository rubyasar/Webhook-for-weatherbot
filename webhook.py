import json
import os
import requests
import datetime
from dateutil import parser

from flask import Flask
from flask import request
from flask import make_response

app=Flask(__name__)
@app.route('/webhook',methods=['Post'])
def webhook():
	req=request.get_json(silent=False,force=True)
	print(json.dumps(req,indent=4))
	
	res=makeResponse(req)
	res=json.dumps(res,indent=4)
	r=make_response(res)
	r.headers['Content-Type']='application/json'
	return r

def makeResponse(req):
	queryResult=req.get("queryResult")
	parameters=queryResult.get("parameters")
	geocity=parameters.get("geo-city")
	date=parameters.get("date")
	dt = parser.parse(date)
	now = datetime.datetime.now()
	naive = now.replace(tzinfo=None)
	cnt=dt.replace(tzinfo=None)-now
	
	r=requests.get("https://samples.openweathermap.org/data/2.5/forecast/daily?q="+geocity+"&appid=b6907d289e10d714a6e88b30761fae22")
	json_object=r.json()
	ls=json_object['list']	
	condition=ls[cnt.days]['weather'][0]['description']	
	speech="The forecast for the "+geocity+" for "+ date+" is "+condition
	
	return{
	"speech":speech,
	"fulfillmentText":speech,
	"source":""}
	
if __name__=='__main__':
	port=int(os.getenv('PORT',5000))
	print("starting app on the port",port)
	app.run(debug=True,port=port,host='0.0.0.0')
