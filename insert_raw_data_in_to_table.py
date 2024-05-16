import mysql.connector
import sys
import os
import json
import csv
from datetime import datetime

pName = sys.argv[1]
dt = sys.argv[2]

# Parse the input date string into a datetime object
date_obj = datetime.strptime(dt, '%Y%m%d')
# Format the datetime object as 'd m Y'
formatted_date = date_obj.strftime('%d/%m/%Y')
print(formatted_date)

tableName= pName + "_" + dt
csvPath = "attachment/"+ dt + "/" + tableName +".csv"
if pName == "loopme":
    csvPath = "attachment/"+ dt + "/1_" + tableName +".csv"
    csvPath_2 = "attachment/"+ dt + "/2_" + tableName +".csv"


print(sys.argv)
with open('conf.json') as f:
    config = json.load(f)
    #print(config)

with open(os.path.dirname(__file__) + '/config/' + pName + '/tbl_structure.json') as f:
    schema = json.load(f)
    #print(schema)


sys.path.append(os.path.join(os.path.dirname(__file__), 'common'))
from mysql_connector import connection
#print(connection)






#create table if not exist for current date
def createCurrentTable(parnerName):
    returnVal = parnerName
    if connection.is_connected():
        print('Connected to MySQL database')
        try:
            # Create a cursor object
            cursor = connection.cursor()
            columns = ''
            for schemaData in schema:
                if schema[schemaData]["type"] == "STRING":
                    columns = columns + " , " + schema[schemaData]["column"] + " VARCHAR(256) " 
                if schema[schemaData]["type"] == "INTEGER":
                    columns = columns + " , " + schema[schemaData]["column"] + " INT(20) " 
                if schema[schemaData]["type"] == "FLOAT":
                    columns = columns + " , " + schema[schemaData]["column"] + " DOUBLE " 
                if schema[schemaData]["type"] == "TIMESTAMP":
                    columns = columns + " , " + schema[schemaData]["column"] + " TIMESTAMP NULL DEFAULT NULL "  
 
            create_table_query = "CREATE TABLE IF NOT EXISTS tbl_" + tableName + " ( id INT AUTO_INCREMENT PRIMARY KEY " + columns + ")"
            
            # print(create_table_query)
            # Execute the CREATE TABLE statement
            cursor.execute(create_table_query)

            # Commit the transaction
            connection.commit()

        except mysql.connector.Error as error:
            print("Failed to insert row:", error)
            returnVal = "Failed"
        finally:
            # Close the cursor and connection
            cursor.close()
            #connection.close()
  
    return returnVal



#insert data into table
def insertIntoRowTable(data,parnerName):
    test=parnerName
    return True




returnVal = createCurrentTable(pName)
#print("RETRUN VAL " + returnVal)

if returnVal != "Failed":
    print(csvPath)
    #call function to get csv data
    cnt=0
    insKey=''
    insVal=''
    for schemaData in schema:
        insKey = insKey + schema[schemaData]["column"] + ","
        insVal = insVal + "%s ,"
        
    insVal = insVal[:-1]
    insKey = insKey[:-1]

    insert_query = "INSERT INTO tbl_" + tableName + " (" + insKey + ") VALUES (" + insVal + ")"

    #print(" INSERT QUERY --------" )
    #print(insert_query)
    
    

    
    cursor = connection.cursor()
    with open(csvPath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row if it exists
        
        # Extract data from the CSV file
        #data = [tuple(row) for row in csv_reader ]  # Convert each row to a tuple
        
        # Extract data from the CSV file, handling blank values for integer columns
        data = []
        for row in csv_reader:
            # Convert each column to the appropriate data type
            cleaned_row = []
            for value in row:
                if value == "": 
                    cleaned_row.append(0)
                else:
                    if value == 0: 
                        cleaned_row.append(value)
                    else:
                        cleaned_row.append(value)

            data.append(tuple(cleaned_row))  # Convert each row to a tuple and add it to the data list

        #print(data)
        # Execute the SQL INSERT query with multiple parameter sets
        cursor.executemany(insert_query, data)

        # Commit the transaction
        connection.commit()

    if pName == "loopme":
        cursor = connection.cursor()
        with open(csvPath_2, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header row if it exists
            
            # Extract data from the CSV file
            #data = [tuple(row) for row in csv_reader ]  # Convert each row to a tuple
            
            # Extract data from the CSV file, handling blank values for integer columns
            data = []
            for row in csv_reader:
                # Convert each column to the appropriate data type
                cleaned_row = []
                for value in row:
                    if value == "": 
                        cleaned_row.append(0)
                    else:
                        if value == 0: 
                            cleaned_row.append(value)
                        else:
                            cleaned_row.append(value)

                data.append(tuple(cleaned_row))  # Convert each row to a tuple and add it to the data list

            #print(data)
            # Execute the SQL INSERT query with multiple parameter sets
            cursor.executemany(insert_query, data)

            # Commit the transaction
            connection.commit()

    

print(returnVal)


#example of command : python3 insert_raw_data_in_to_table.py equativ 20240511
#example of command : python3 insert_raw_data_in_to_table.py smaato 20240511
#example of command : python3 insert_raw_data_in_to_table.py loopme 20240511