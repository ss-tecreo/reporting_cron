import mysql.connector
import sys
import os
import json
import csv
import datetime
import argparse
import shutil


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
else:
    #date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
    dt = (datetime.date.today() - datetime.timedelta(int(noOfPreviousDay))).strftime("%Y%m%d")



pName = args.pname
tableName= pName + "_" + dt

print(tableName)
#=====================================
# Specify the source and destination directories
source_directory = os.path.dirname(__file__) + "/attachment"
destination_directory = os.path.dirname(__file__) + "/attachment/" + dt


def check_csv_has_data(file_path):
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"The file '{file_path}' does not exist.")
        return False
    
    try:
        with open(file_path, 'r') as file:
            # Read the first non-empty line (header)
            header = file.readline().strip()
            
            # Check if there's a header
            if not header:
                print(f"The CSV file '{file_path}' is empty.")
                return False
            
            # Check if there's at least one more line after the header
            for line in file:
                if line.strip():  # Ignore empty lines
                    print(f"The CSV file '{file_path}' has data.")
                    return True
            
            # If no data lines are found
            print(f"The CSV file '{file_path}' has only a header and no data.")
            return False
    except Exception as e:
        print(f"An error occurred while checking the file: {e}")
        return False

# Example usage
#file_path = 'your_file.csv'
#has_data = check_csv_has_data(file_path)
#print(f"Has data: {has_data}")



# Check if the directory exists
if not os.path.exists(destination_directory):
    # Create the directory
    os.makedirs(destination_directory)
    print(f"Directory '{destination_directory}' created successfully")
else:
    print(f"Directory '{destination_directory}' already exists")

# Get a list of files in the source directory
files = os.listdir(source_directory)

fileNamePostfix = ".csv"
fileNamePrefix = pName + "_" + dt
# Iterate over each file in the source directory
cnt = 1
for file_name in files:
    ink_file_name = ""
    destination_directory_path= ""
    if fileNamePrefix in file_name and fileNamePostfix in file_name:
        source_file_path = os.path.join(source_directory, file_name)
        if os.path.isfile(source_file_path):
            fileDataMsg = ""
            if check_csv_has_data(source_file_path):
                if pName == "loopme":
                    ink_file_name = str(cnt) + "_" + tableName +".csv"
                    cnt=cnt+1
                else:
                    ink_file_name = tableName +".csv"
                destination_directory_path = os.path.join(destination_directory, ink_file_name)
                #print(ink_file_name)
                #print("source_file_path")
                #print(source_file_path)
                #print(destination_directory_path)
                shutil.move(source_file_path, destination_directory_path)
        print(file_name)
    else:
        print("End of file")
#======================================
csvPath = os.path.dirname(__file__) + "/attachment/"+ dt + "/" + tableName +".csv"

if pName == "loopme":
    csvPath = os.path.dirname(__file__) + "/attachment/"+ dt + "/1_" + tableName +".csv"
    csvPath_2 = os.path.dirname(__file__) + "/attachment/"+ dt + "/2_" + tableName +".csv"


#print(sys.argv)
with open(os.path.dirname(__file__) + '/conf.json') as f:
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
            connection.close()
        finally:
            # Close the cursor and connection
            cursor.close()
            #connection.close()
  
    return returnVal




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
    
    
    def insertData(insert_query , data , cnt):
        print("-----------------HI-----------------")
        print(cnt)
        print(insert_query)
        print("-----------------HI-----------------")
        #print(data)
        # Execute the SQL INSERT query with multiple parameter sets
        cursor.executemany(insert_query, data)

        # Commit the transaction
        connection.commit()

    

    cursor = connection.cursor()
    with open(csvPath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row if it exists
        
        # Extract data from the CSV file
        #data = [tuple(row) for row in csv_reader ]  # Convert each row to a tuple
        
        # Extract data from the CSV file, handling blank values for integer columns
        data = []
        cnt=0
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
            cnt = cnt+1
            if cnt > 5000 :
                insertData(insert_query , data , cnt)
                data = []
                cnt=0
        if cnt > 0 :
            insertData(insert_query , data , cnt)
            data = []
            cnt=0
        




    if pName == "loopme":
        cursor = connection.cursor()
        with open(csvPath_2, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header row if it exists
            # Extract data from the CSV file, handling blank values for integer columns
            data = []
            cnt=0
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
                cnt = cnt+1
                if cnt > 5000 :
                    insertData(insert_query , data , cnt)
                    data = []
                    cnt=0
            if cnt > 0 :
                insertData(insert_query , data , cnt)
                data = []
                cnt=0



print(returnVal)


#example of command : ~/.venvs/foo/bin/python3 insert_raw_data_in_to_table.py --since 1 --pname equativ --date 20240511
#example of command : ~/.venvs/foo/bin/python3 insert_raw_data_in_to_table.py --since 1 --pname smaato --date 20240511
#example of command : ~/.venvs/foo/bin/python3 insert_raw_data_in_to_table.py --since 1 --pname loopme
