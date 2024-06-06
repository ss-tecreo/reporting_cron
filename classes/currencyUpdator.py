#
# https://app.exchangerate-api.com/keys
# sudhanshu@tecreo.io tecReoSud@24
# url https://v6.exchangerate-api.com/v6/0a4efe25aae453e48fd96058/latest/USD
# 0a4efe25aae453e48fd96058
#

import sys
import os
import json
import datetime
import requests



# class for get currency updated value for calculation (Base is USD)#
class CURRENCYLAYER:
    def __init__(apiUrl,currencyBase):
        print(currencyBase);
        print("---------------");

    def greet(apiUrl , input_array):
        apiPath='https://v6.exchangerate-api.com/v6/0a4efe25aae453e48fd96058/latest/USD';
        res = requests.get(apiPath)
        data = res.json()
        #print(data)
        for resArr in input_array:
            input_array[resArr] = data['conversion_rates'][resArr]
        return input_array

    def greet_EUR(apiUrl ,input_array):
        apiPath = 'http://api.exchangeratesapi.io/v1/latest?access_key=66cd72ca9b1aa72a071e4f7b2d5e3e91';
        #print(currencyBase)
        res = requests.get(apiPath)
        data = res.json()
        #print(data)
        for resArr in input_array:
            input_array[resArr] = data['rates'][resArr]
        return input_array




##finalData={}
##input_array = {'INR': '', 'EUR': 'USD'}
# Create an instance of the class
##currObj = CURRENCYLAYER('USD')
#print(currObj)
##input_array = {'INR': '', 'EUR': 'USD'}
# Call the method of the class
##json_data_USD = currObj.greet(input_array)
#print(json_data_USD)
##finalData["USD_INR"]=json_data_USD["INR"];

# Create an instance of the class
##currObjEUR = CURRENCYLAYER('EUR')
##json_data_EUR = currObjEUR.greet_EUR(input_array)
#print(json_data_EUR)

#y = json.loads(json_data_USD)
#print(json_data_USD["INR"])
##finalData["EUR_INR"]=json_data_EUR["INR"];

#print(finalData)
