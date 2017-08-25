
# coding: utf-8

# In[1]:

import os
import json

import numpy as np
import pandas as pd
from math import sqrt
import re


with open('restaurants_dish.json', 'r') as f:
     restaurants_dish = json.load(f)




# In[90]:

#when customer calls a restaurant name, return the restaurant info
#print([i for i in restaurants_dish if i['name']=='Barrel Head Brewhouse'])


# In[93]:

##start using the flask to call contents from the html web
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("website.html")

@app.route('/submit', methods=['POST','GET'])
def my_form_post():
    recommended_restaurants_formatted=[]
    if request.method=='POST':
        text = request.form['text']
 
        recommended_restaurants=[]
        for i in restaurants_dish:
            recommended_restaurants.append(list(set([(i['Name'], i['Overall Rating'],i['Total Number of Reviews'],float(i['Wilson Score']), i['Restaurant Link']) for s in i['Recommended Dish'] 
                                            if text in s[0]])))
        recommended_restaurants=sum([x for x in recommended_restaurants if x != []], [])                                                                    
        recommended_restaurants=sorted(recommended_restaurants, key=lambda x: x[-2], reverse=True)

        for i in recommended_restaurants:
            recommended_restaurants_formatted.append([i[0], "Yelp's Rating"+': '+  i[1],"Rachel's Rating"+': ' + str(round((i[-2])*100)),
                                              [s['Recommended Dish'] for s in restaurants_dish if i[0] in s['Name']][0],i[-1] ])

        for i in recommended_restaurants_formatted:
            i[3]=[j[0] for j in i[3]]

    return render_template("website.html", recommendation=recommended_restaurants_formatted)


if __name__ == '__main__':
    app.run()


