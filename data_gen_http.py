import math
import numpy as np
import pandas as pd
from datetime import datetime
from calendar import timegm
from bottle import (Bottle, HTTPResponse, run, request, response,
                    json_dumps as dumps)
from pandas_datareader import data

tickers = ['AAPL', 'MSFT', '^GSPC']

#FUNCTIONS = {'series A': math.sin, 'series B': math.cos}

app = Bottle()

def create_data_points(name, start, end):  
    #print('start: ', start)
    #print('end: ', end)
    panel_data = data.DataReader(name, 'yahoo', start, end)
    #print(panel_data)
    #print(list(zip(panel_data['Close'],panel_data.index.astype(np.int64) // 10**6)))
    return list(zip(panel_data['Close'],panel_data.index.astype(np.int64) // 10**6))


@app.hook('after_request')
def enable_cors():
    #print("after_request hook")
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = \
        'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@app.route("/", method=['GET', 'OPTIONS'])
def index():
    return "OK"


@app.post('/search')
def search():
    return HTTPResponse(body=dumps(tickers),
                        headers={'Content-Type': 'application/json'})


@app.post('/query')
def query():
        #print(request.json)
    

        body = []
        start, end = request.json['range']['from'], request.json['range']['to']
        for target in request.json['targets']:
            name = target['target']
            datapoints = create_data_points(name, start, end)
            body.append({'target': name, 'datapoints': datapoints})
            

        body = dumps(body)
        #print('body: ', body)
        return HTTPResponse(body=body,
                        headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    run(app=app, host='localhost', port=8081)
