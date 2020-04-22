from flask import Flask, jsonify,request
from MNBPickleReader import get_final_output, predict,get_url
import MNBPickleReader
from scrapping import get_url

import time
import pickle
import sklearn
import numpy as np
import json
app = Flask(__name__);
@app.route('/api', methods=['GET'])
def hello_world():
	Input = request.args['Query']
	d={}

	userInput = json.loads(Input)
	print(userInput)
	


	# data = json.loads(d)

	# if userInput['process'] == 'postal_code':
	# 	d = get_url(userInput['input'])
	# elif userInput['process'] == 'identification':
	# 	d = return_url(userInput['input'], 'Oshawa')
	# 	pass
	if userInput['process'] == 'postal_code':
		response = get_url(userInput['input'])
		if response['status'] == False:   
			d = {"message" : response['response'], "process" : "postal_code","processValid" : True, "status" : response['status']}
		else:
			d = {"message" : response['response'], "process" : "identification","processValid" : True, "status" : response['status']}
			pass
	else:
		d= predict(userInput['input'], 'Oshawa');
		pass
	print(d)

	print(d)
	#d['Query']=str(time.ctime())
	data = json.loads(json.dumps(d))
	return data



# @app.route("/bot", methods=["POST"])
# def response():

#     query = dict(request.form)['query']
#     res = query + " " + time.ctime()
#     return jsonify({"response" : res})
if __name__=="__main__":
    app.run()