#!/usr/local/opt/python/Frameworks/Python.framework/Versions/3.7/bin/python3
# -*- coding: utf-8 -*-
import os
import json
import string
import csv
import requests
from flask import Flask, render_template, jsonify, make_response,request
from flask_restful import Resource, Api, reqparse
import logging
from logging.handlers import TimedRotatingFileHandler


TOKEN = '8311afc7a6b443d5813616cd7adfc07d'
LOG_DIR = '/Users/timmy/api.log'
csv_file = 'top-1k-ingredients.csv' 
app = Flask(__name__)
api = Api(app)

@app.route('/ingredients')
def get_Top1K_Ingredients():
    '''
    curl http://10.110.214.212:5052/ingredients
    get the top 1k ingredients in the local csv file ,you need update csv file every once perior time;
    '''
    ingredients_data = []
    ingredients_dict = {}
    with open(csv_file) as csvfile:
        csv_reader = csv.reader(csvfile)  
        ingredients_header = next(csv_reader)  
        for row in csv_reader:  
            str_row = row[:][0]
            append_row = str_row.split(";")[0]
            ingredients_data.append(append_row)
        print(ingredients_data)
        ingredients_dict['data'] = ingredients_data
    return jsonify(ingredients_dict)



@app.route('/recipes/<ingredients>')
def get_recipes(ingredients):
    '''
    curl http://10.110.214.212:5052/recipes/apples,+flour,+sugar
    '''
#    URL = https://api.spoonacular.com/recipes/findByIngredients?ingredients=apples,+flour,+sugar&number=2&apiKey=8311afc7a6b443d5813616cd7adfc07d    
    response = {}
    URL = 'https://api.spoonacular.com/recipes/findByIngredients?' + 'ingredients=' + ingredients + '&number=10'+ '&apiKey=' + TOKEN
    headers = {'content-type': 'application/json'}
    r = requests.get(URL, headers=headers)
    print(json.loads(r.text))
    response['data'] = json.loads(r.text)
    return jsonify(response)

@app.route('/popular_recipes/<ingredients>')
def get_popular_recipes(ingredients):
    response = {}
    response_list = []
    URL1 = 'https://api.spoonacular.com/recipes/findByIngredients?' + 'ingredients=' + ingredients + '&number=10'+ '&apiKey=' + TOKEN
    headers = {'content-type': 'application/json'}
    r1 = requests.get(URL1, headers=headers)
    for i in json.loads(r1.text):
        new_dict = {}
        recipe_id = i['id']
        URL2 = 'https://api.spoonacular.com/recipes/'+ str(recipe_id) + '/information?&apiKey=' + TOKEN
        r2 = requests.get(URL2, headers=headers)
        if json.loads(r2.text)['veryPopular'] == True:
            response_list.append(i)
        response['data'] = response_list
    print(response) 
    return jsonify(response)




if __name__ == '__main__':
    logHandler = TimedRotatingFileHandler(LOG_DIR, when='D', backupCount=7)
    logFormatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logHandler.setFormatter(logFormatter)
    logger = logging.getLogger("api_info")
    logger.addHandler(logHandler)
    logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=5052)
