import pandas as pd
import numpy as np
from datetime import datetime,timedelta
from sklearn.metrics import mean_squared_error
from scipy.optimize import curve_fit
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import requests
import datetime
import json 
from flask import Flask,jsonify,request
from datetime import timedelta, date


app = Flask(__name__)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
def logistic_model(x,a,b,c):
    return c/(1+np.exp(-(x-b)/a))

@app.route('/predict', methods=['GET'])
def predict():
    data = requests.get("https://indonesia-covid-19.mathdro.id/api")
    casebyday = requests.get('https://indonesia-covid-19.mathdro.id/api/harian')
    x = []
    y = [0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,]
    for aa in casebyday.json()['data']:
    #    x.append(aa['harike'])
        y.append(aa['jumlahKasusKumulatif'])
    y.pop()
    x = []
    i = 0
    for aaa in y:
        x.append(i)
        i+=1

    fit = curve_fit(logistic_model,x,y,p0=[2,100,1000])
    A,B=fit
    errors = [np.sqrt(fit[1][i][i]) for i in [0,1,2]]
    a=A[0]+errors[0]
    b=A[1]+errors[1]
    c=A[2]+errors[2]
    sol = int(fsolve(lambda x : logistic_model(x,a,b,c) - int(c),b))
    start_date = "22/01/20"
    date_1 = datetime.datetime.strptime(start_date, "%d/%m/%y")
    end_date = date_1 + timedelta(days=sol)
    x=end_date.strftime("%d %b %Y")
    # print("Jumlah kasus maksimal di indonesia menurut prediksi adalah {:f}".format(A[2]+errors[2])) #Penambahan dengan error
    # print("Wabah akan berakhir {:.0f} hari setelah 22 Januari 2020 atau {}". format(sol,x))
    outputs = dict()
    outputs['max_case'] = A[2]+errors[2]
    outputs['max_day'] = sol
    outputs['end_date'] = x
    return jsonify(outputs)

if __name__ == '__main__':
    app.run(port="5002",host="0.0.0.0",debug=True)