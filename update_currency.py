import mysql.connector
import sys
import os
import json

with open(os.path.dirname(__file__) + '/conf.json') as f:
    config = json.load(f)
    #print(config)


# Add the relative path to the directory containing .py
sys.path.append(os.path.join(os.path.dirname(__file__), 'classes'))
#import currencyUpdator.py
from currencyUpdator import CURRENCYLAYER



finalData={}
input_array = {'INR': '', 'EUR': 'USD'}
# Create an instance of the class
currObj = CURRENCYLAYER('USD')
# Call the method of the class
json_data_USD = currObj.greet(input_array)
#print(json_data_USD)

finalData["USD_INR"]=json_data_USD["INR"];

# Create an instance of the class
currObjEUR = CURRENCYLAYER('EUR')
json_data_EUR = currObjEUR.greet_EUR(input_array)
print(json_data_EUR)

#y = json.loads(json_data_USD)
#print(json_data_USD["INR"])
finalData["EUR_INR"]=json_data_EUR["INR"];
print(finalData)


#=====================================
# Create an instance of the class
##currObj = CURRENCYLAYER('test')
#print(currObj)
##input_array = {'INR': '', 'EUR': ''}
# Call the method of the class
##json_data = currObj.greet(input_array)
#print(json_data)
#=====================================


sys.path.append(os.path.join(os.path.dirname(__file__), 'common'))
from mysql_connector import connection
print(connection)



# Check if connection is successful
if connection.is_connected():
    print('Connected to MySQL database')

    try:
        # Create a cursor object
        cursor = connection.cursor()

        # Define the INSERT INTO statement
        insert_query = "INSERT INTO tbl_currency (USD_INR, EUR_INR,updatedOn) VALUES (%s, %s,NOW())"
        values = []
        # Define the values to insert
        #for data in json_data:
            #print(json_data[data])
        values.append((finalData["USD_INR"], finalData["EUR_INR"]))
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

#example : python3 update_currency.py
