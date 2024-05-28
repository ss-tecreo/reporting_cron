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
    def __init__(apiUrl,val):
        apiUrl.val = 'https://v6.exchangerate-api.com/v6/0a4efe25aae453e48fd96058/latest/USD';
        #print(apiUrl.val)

    def greet(apiUrl,input_array):
        print(apiUrl)
        res = requests.get(apiUrl.val)
        data = res.json()
        #print(data)
        for resArr in input_array:
            input_array[resArr] = data['conversion_rates'][resArr]
        return input_array









