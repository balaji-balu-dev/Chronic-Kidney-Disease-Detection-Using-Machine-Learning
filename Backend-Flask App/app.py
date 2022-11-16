import requests
import pandas as pd
import numpy as np

from flask import Flask, request, render_template, url_for, redirect
import pickle
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "YbH1Jt5lA7lHvNhNPEUuKjdais91dxeOYYnHDbLraG2b"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

#initializing a flask app
app = Flask(__name__)

#Loading the model
model = pickle.load(open('CKD.pkl', 'rb'))

#route to display the homepage
@app.route('/')
def home():
    return render_template('home.html')  #rendering the home page
    
@app.route('/Prediction', methods = ['POST','GET'])
def prediction():  #Route to display the prediction page 
    return render_template('indexnew.html')
@app.route('/Home', methods = ['POST','GET'])
def my_home():
    return render_template('home.html')

@app.route('/predict', methods = ['POST'])  #route to show the predictions in the web UI 
def predict():

    #reading inputs given by the user
    
    blood_urea = request.form["blood_urea"]
    blood_glucose_random = request.form["blood glucose random"]
    coronary_artery_disease = request.form["coronary_artery_disease"]
    anemia = request.form["anemia"]
    pus_cell = request.form["pus_cell"]
    red_blood_cells = request.form["red_blood_cells"]
    diabetesmellitus = request.form["diabetesmellitus"]
    pedal_edema = request.form["pedal_edema"]

    if (coronary_artery_disease == 'Yes'):
        c1 = 1
    else:
        c1 = 0
    if (anemia == 'Yes'):
        a1 = 1
    else:
        a1 = 0
    if (pus_cell == 'Normal'):
        p1 = 1
    else:
        p1 = 0
    if (red_blood_cells == 'Normal'):
        r1 = 1
    else:
        r1 = 0
    if(diabetesmellitus == 'Yes'):
        d1 = 1
    else:
        d1 = 0
    if(pedal_edema == 'Yes'):
        p2 = 1
    else:
        p2 = 0
    
    t = [[int(blood_urea),int(blood_glucose_random),int(c1),int(a1),int(p1),int(r1),int(d1),int(p2)]]
    print(t)
           
    payload_scoring = {"input_data": [{"field": [['blood_urea','blood glucose random','coronary_artery_disease','anemia','pus_cell',
    'red_blood_cells','diabetesmellitus','pedal_edema']], "values": t}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/22964015-8997-4dc4-a352-f309cbc4907c/predictions?version=2022-11-11', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    pred = predictions['predictions'][0]['values'][0][0]
    print(pred)

    
     
    return render_template('result.html',pred = pred)

if __name__ == '__main__':
    app.run(debug = True)   #Running the app
