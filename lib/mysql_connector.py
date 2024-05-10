import mysql.connector
import sys
import os
import json
import datetime

currDate = datetime.date.today().strftime("%Y%m%d")

#print(os.path.dirname(__file__))
with open(os.path.dirname(__file__) + '/../conf.json') as f:
    config = json.load(f)
#print(config["mysqlConf"])

#with open(os.path.dirname(__file__) + '/../config/equativ.json') as f:
#    schema = json.load(f)

connection = mysql.connector.connect(
    host=config["mysqlConf"]["host"], 
    user=config["mysqlConf"]["user"], 
    password=config["mysqlConf"]["password"], 
    database=config["mysqlConf"]["database"]
)
#print(connection)

