import json
import os
import requests
import datetime

from flask import Flask
from flask import request
from flask import make_response

app=Flask(__name__)
@app.route('/webhook',methods=['Post'])
def webhook():
	req=request.get_json(silent=True,force=True)
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
	now = datetime.datetime.now()
	cnt=date-now
	
	r=requests.get("http://api.openweathermap.org/data/2.5/forecast/daily?q="+city+"&cnt="+cnt+"&appid=a28c94ceb5c94ddb9beb8780a7eb4b1c")
	json_object=r.json()
	ls=json_object['list']	
	condition=ls[cnt]['weather'][0]['description']	
	speech="The forecast for the "+city+" for "+ date+" is "+condition
	
	return{
	"speech":speech,
	"displayText":speech,
	"source":""}
	
if __name__=='__main__':
	port=int(os.getenv('PORT',5000))
	print("starting app on the port",port)
	app.run(debug=False,port=port,host='0.0.0.0')