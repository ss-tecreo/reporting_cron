import mysql.connector
import sys
import os
import json
import csv
import re
import datetime
import argparse
import shutil

#from datetime import datetime


# command line argument settings
parser = argparse.ArgumentParser()
parser.add_argument('--since', required=False, dest='days', type=str, help='provide a number to insert data from date - "1" ')
parser.add_argument('--pname', required=True, dest='pname', type=str, help='provide supply partner name "equative"')
parser.add_argument('--date', required=False, dest='date', type=str, help='provide report date date "20240515" ')
args = parser.parse_args()
if args.days is not None:
    noOfPreviousDay = args.days
else:
    noOfPreviousDay = 1

if args.date is not None:
    dt = args.date
    formatted_date = (datetime.date.today() - datetime.timedelta(0)).strftime("%Y-%m-%d")
else:
    formatted_date = (datetime.date.today() - datetime.timedelta(int(noOfPreviousDay))).strftime("%Y-%m-%d")
    #date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
    dt = (datetime.date.today() - datetime.timedelta(int(noOfPreviousDay))).strftime("%Y%m%d")


pName = args.pname
destTableName = "tbl_aggregated_daily"


print("FORMATED DATE ")
print(formatted_date)
# Convert to datetime object
#date_object = datetime.strptime(dt, "%Y%m%d")

# Convert back to string with desired format
#formatted_date = date_object.strftime("%Y-%m-%d")
#print(formatted_date)


with open(os.path.dirname(__file__) + '/conf.json') as f:
    config = json.load(f)
    #print(config)

#print(sys.argv)


sys.path.append(os.path.join(os.path.dirname(__file__), 'common'))
from mysql_connector import connection
#print(connection)



#insert data into table
def insertIntoAggregatedTable(parnerName):
    # Create a cursor object
    cursor = connection.cursor()
    # Read SQL queries from the .sql file
    with open(os.path.dirname(__file__) + "/config/" + parnerName + "/query.sql", "r") as file:
        queries = file.read()
    queries = queries.replace("[REPORT_DATE]", dt)
    queries = queries.replace("[REPORT_DATE_FORMATED]", formatted_date)
    print(queries) 
    # Execute the SQL INSERT INTO statement
    cursor.execute(queries)

    # Commit the transaction
    connection.commit()

    # Close the cursor and connection
    cursor.close()

    return True


insertIntoAggregatedTable(pName)


# example : 
# ~/.venvs/foo/bin/python3 aggregate_data.py --pname smaato --date 20240513
# ~/.venvs/foo/bin/python3 aggregate_data.py --pname loopme --date 20240513
# ~/.venvs/foo/bin/python3 aggregate_data.py --pname equativ --date 20240513 
