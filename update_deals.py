import mysql.connector
import sys
import os
import json

with open(os.path.dirname(__file__) + '/conf.json') as f:
    config = json.load(f)
    #print(config)


sys.path.append(os.path.join(os.path.dirname(__file__), 'common'))
from mysql_connector import connection
print(connection)



# Check if connection is successful
if connection.is_connected():
    print('Connected to MySQL database')

    try:
        # Create a cursor object
        cursor = connection.cursor()


        insert_query = ( 'INSERT INTO tbl_client_deal (client_id,supply_partner,deal_id,deal_name)  SELECT 0 as client_id , supply_partner , "" as deal_id , deal_name FROM tbl_aggregated_daily ON DUPLICATE KEY UPDATE updatedAt=NOW() ')
        print(insert_query)
        #print(values)
        # Execute the INSERT INTO statement
        cursor.execute(insert_query)

        # Commit the transaction
        connection.commit()

        print("Row Inserted/Updated Successfully.")
    except mysql.connector.Error as error:
        print("Failed to insert row:", error)
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
else:
    print('Connection failed.')

#example : python3 update_currency.py
