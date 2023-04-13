import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from flask_cors import CORS, cross_origin
import json
from urllib.parse import urlparse
#load model
app = Flask(__name__)
CORS(app)

#  Requirements
black = pd.read_csv("C:\\Users\\YASHASVI\\OneDrive\\Desktop\\Phishing URL Detector\\Implementation\\Level 1\\Blacklisted.csv")
white = pd.read_csv("C:\\Users\\YASHASVI\\OneDrive\\Desktop\\Phishing URL Detector\\Implementation\\Level 1\\whitelisted.csv")
l2_model = pickle.load(open("L2_phishing_model.pkl","rb"))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    # URL from the user
    body = request.get_json()
    print(body)
    urls = body['URL']
    
    response = []
    for url in urls:
        ####################################################################### Level 1 WhiteList and BlackList module
        url_parse = urlparse(url)
        domain = url_parse.netloc
        
        whiteList = white.applymap(lambda x: domain in str(x)).any().any()
        blackList = black.applymap(lambda x: domain in str(x)).any().any()
        
        if whiteList:
            response.append({"url":url,"type":"Legitimate"})
            continue
        
        if blackList:
            response.append({"url":url,"type":"Phishing"})
            continue
        l2_prediction = l2_model.predict([url])
        if l2_prediction == "bad":
            response.append({"url":url,"type":"Phishing"})
            continue
        else:
            response.append({"url":url,"type":"Legitimate"})
            continue
        
        ######################################################################### End of Level 2 and 3
    data = {"response":response}
    print(response)

    return jsonify(data)
####### Flask Server 

if __name__ == "__main__":
    app.run( debug=True)

