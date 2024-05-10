#
#https://currencylayer.com/quickstart
#sudhanshu@chocolateplatform.com 123456
#ecef474bf99dbc1648c42b576346f240
#

import sys
import os
import json
import datetime
import requests

# class for get currency updated value for calculation (Base is USD)#
class CURRENCYLAYER:
    def __init__(apiUrl,val):
        apiUrl.val = 'http://api.currencylayer.com/live?access_key=ecef474bf99dbc1648c42b576346f240&format=1';

    def greet(apiUrl,input_array):
        res = requests.get(apiUrl.val)
        data = res.json()
        #print(data)
        for resArr in input_array:
            input_array[resArr] = data['quotes']['USD'+resArr]
        return input_array









