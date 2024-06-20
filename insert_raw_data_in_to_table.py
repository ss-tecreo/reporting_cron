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
tableName= pName + "_" + dt;
print(tableName);

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


#functions 
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

#End of function def check_csv_has_data:

# Example usage
#file_path = 'your_file.csv'
#has_data = check_csv_has_data(file_path)
#print(f"Has data: {has_data}")


#-------------------------------------------
#create table if not exist for current date
def createCurrentTable(partnerName):
    returnVal = partnerName
    if connection.is_connected():

        print('Connected to MySQL database for create new table ')
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
            print("Failed to Create table:", error)
            returnVal = "Failed"
            connection.close()
        finally:
            # Close the cursor and connection
            cursor.close()
            #connection.close()  
    return returnVal

#End of function def createCurrentTable(partnerName):

columnNotInDB=[]
# -------------------------------------------
def insertIntoTable(source_file_path):
    if connection.is_connected():
        returnVal = "insert";
        try:
            insKey=''
            insVal=''

            with open(source_file_path, mode='r', encoding='utf-8-sig' , newline='') as file:
                reader = csv.reader(file)
                headers = next(reader)
                print(headers)
            tmpCnt=0
            
            for headersCol in headers:
                if headersCol in schema:
                    insKey = insKey + schema[headersCol]["column"] + ","
                    insVal = insVal + "%s ,"
                else:
                    columnNotInDB.append(tmpCnt)
                tmpCnt=tmpCnt+1

            
            insVal = insVal[:-1]
            insKey = insKey[:-1]

            insert_query = "INSERT INTO tbl_" + tableName + " (" + insKey + ") VALUES (" + insVal + ")"

            cursor = connection.cursor()
            with open(source_file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                #print(csv_reader);
                next(csv_reader)  # Skip the header row if it exists
                
                # Extract data from the CSV file, handling blank values for integer columns
                data = []
                cnt=0
                
                for row in csv_reader:
                    colCnt=-1
                    #print(row)
                    # Convert each column to the appropriate data type
                    cleaned_row = []
                    for value in row:
                        colCnt=colCnt+1
                        if(colCnt not in columnNotInDB): 
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
        except mysql.connector.Error as error:
            print("Failed to insert row:", error)
            returnVal = "Failed"
            connection.close()
        finally:
            # Close the cursor and connection
            cursor.close()
            #connection.close()
    return returnVal

# End of function insertIntoTable
#--------------------------------------------

def insertData(insert_query , data , cnt):
    print("-----------------HI-----------------")
    #print(data)
    print(insert_query)
    print("-----------------HI-----------------")
    #print(data)
    # Execute the SQL INSERT query with multiple parameter sets
    cursor = connection.cursor();
    cursor.executemany(insert_query, data)

    # Commit the transaction
    connection.commit()

#end of function insertData
#--------------------------------------------


#=====================================
# Specify the source and destination directories
source_directory = os.path.dirname(__file__) + "/attachment"
destination_directory = os.path.dirname(__file__) + "/attachment/" + dt
fail_directory = os.path.dirname(__file__) + "/attachment/fail/" + dt

# Check if the directory exists
if not os.path.exists(fail_directory):
    # Create the directory
    os.makedirs(fail_directory)

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

isTableCreated = createCurrentTable(pName)
#print("RETRUN VAL " + returnVal)

if isTableCreated != "Failed":
    for file_name in files:
        ink_file_name = ""
        destination_directory_path= ""
        fail_directory_path="";
        fail_directory_path = os.path.join(fail_directory, ink_file_name)
        if fileNamePrefix in file_name and fileNamePostfix in file_name:
            source_file_path = os.path.join(source_directory, file_name)
            if os.path.isfile(source_file_path):
                fileDataMsg = ""
                if check_csv_has_data(source_file_path):
                    destination_directory_path = os.path.join(destination_directory, ink_file_name)

                    #call function insert into table
                    if insertIntoTable(source_file_path) != "Failed":
                        shutil.move(source_file_path, destination_directory_path)
                    else:
                        #move to fail path
                        shutil.move(source_file_path, fail_directory_path)
                        print("FAIL -- insertIntoTable ")
                else:
                    #move to fail path
                    shutil.move(source_file_path, fail_directory_path)
                    print("FAIL -- check_csv_has_data ")
            else:
                #move to fail path
                shutil.move(source_file_path, fail_directory_path)
                print("FAIL -- isfile ")

#end of if isTableCreated
#----------------------------------------------------------------------------------------------
                

# read all .csv for the partner one by one 
    # createCurrentTable if not exist   
    # Insert into table
    # if inserted succesfully then move to date folder
    # else move to fail folder 

### =========================================================== ###



#example of command : ~/.venvs/foo/bin/python3 insert_raw_data_in_to_table.py --since 1 --pname equativ --date 20240511
#example of command : ~/.venvs/foo/bin/python3 insert_raw_data_in_to_table.py --since 1 --pname smaato --date 20240511
#example of command : ~/.venvs/foo/bin/python3 insert_raw_data_in_to_table.py --since 1 --pname loopme
