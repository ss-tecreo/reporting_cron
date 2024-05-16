import mysql.connector
import sys
import os
import json
import csv
import re
from datetime import datetime


destTableName = "tbl_aggregated_daily"
pName = sys.argv[1]
dt = sys.argv[2]

# Convert to datetime object
date_object = datetime.strptime(sys.argv[2], "%Y%m%d")

# Convert back to string with desired format
formatted_date = date_object.strftime("%Y-%m-%d")

print(formatted_date)



print(sys.argv)
with open('conf.json') as f:
    config = json.load(f)
    #print(config)


sys.path.append(os.path.join(os.path.dirname(__file__), 'common'))
from mysql_connector import connection
print(connection)



#insert data into table
def insertIntoAggregatedTable(parnerName):
    # Create a cursor object
    cursor = connection.cursor()
    # Read SQL queries from the .sql file
    with open("config/" + parnerName + "/query.sql", "r") as file:
        queries = file.read()
    queries = queries.replace("[REPORT_DATE]", dt)
    queries = queries.replace("[REPORT_DATE_FORMATED]", formatted_date)
    
    # Execute the SQL INSERT INTO statement
    cursor.execute(queries)

    # Commit the transaction
    connection.commit()

    # Close the cursor and connection
    cursor.close()

    return True


insertIntoAggregatedTable(pName)