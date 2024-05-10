import mysql.connector
import sys
import os
import json

with open('conf.json') as f:
    config = json.load(f)

#print(config)

# Add the relative path to the directory containing .py
sys.path.append(os.path.join(os.path.dirname(__file__), 'classes'))
#import currencyUpdator.py
from currencyUpdator import CURRENCYLAYER


# Create an instance of the class
currObj = CURRENCYLAYER('test')
#print(currObj)
input_array = {'INR': '', 'EUR': '','MMK':''}
# Call the method of the class
json_data = currObj.greet(input_array)



sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
from mysql_connector import connection
#print(connection)



# Check if connection is successful
if connection.is_connected():
    print('Connected to MySQL database')

    try:
        # Create a cursor object
        cursor = connection.cursor()

        # Define the INSERT INTO statement
        insert_query = "INSERT INTO currency (INR, EUR,USD) VALUES (%s, %s,%s)"
        values = []
        # Define the values to insert
        #for data in json_data:
            #print(json_data[data])
        values.append((json_data["INR"], json_data["EUR"], 1))
        #values = [('USD', 89.45),('EUR', 89.45),('INR', 89.45)]
        # Execute the INSERT INTO statement
        cursor.executemany(insert_query, values)

        # Commit the transaction
        connection.commit()

        print("Row inserted successfully.")
    except mysql.connector.Error as error:
        print("Failed to insert row:", error)
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
else:
    print('Connection failed.')
