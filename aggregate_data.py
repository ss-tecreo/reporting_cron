import mysql.connector
import sys
import os
import json
import csv
import re



destTableName = "tbl_aggregated"
pName = sys.argv[1]
dt = sys.argv[2]



print(sys.argv)
with open('conf.json') as f:
    config = json.load(f)
    #print(config)


sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
from mysql_connector import connection
print(connection)



#insert data into table
def insertIntoAggregatedTable(parnerName):
    # Create a cursor object
    cursor = connection.cursor()
    # Read SQL queries from the .sql file
    with open("config/" + parnerName + ".sql", "r") as file:
        queries = file.read()
    
    #print(queries)
    pattern_to_replace = "[CURR_DT]"
    # Create a regex pattern to match the substring
    pattern = re.compile(re.escape(pattern_to_replace))
    
    # Use re.sub() to replace the substring with the replacement string
    query_string = re.sub(pattern, dt, queries)
    #print(query_string)  # Output: "hello Python"
    
    # Execute the SQL INSERT INTO statement
    cursor.execute(query_string)

    # Commit the transaction
    connection.commit()

    # Close the cursor and connection
    cursor.close()


    test=parnerName
    return True


insertIntoAggregatedTable(pName)