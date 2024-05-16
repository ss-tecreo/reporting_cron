import snowflake.connector

import json
with open('../conf.json') as f:
    config = json.load(f)


def connect_to_snowflake(user, password, account, warehouse, database, schema):
    """
    Connect to Snowflake and return the connection object and cursor.
    
    Parameters:
        user (str): Snowflake username
        password (str): Snowflake password
        account (str): Snowflake account name
        warehouse (str): Snowflake warehouse name
        database (str): Snowflake database name
        schema (str): Snowflake schema name

    Returns:
        (connection, cursor): A tuple containing the Snowflake connection object and cursor.
    """
    # Snowflake connection parameters
    conn_params = {
        'user': user,
        'password': password,
        'account': account,
        'warehouse': warehouse,
        'database': database,
        'schema': schema
    }

    # Connect to Snowflake
    try:
        conn = snowflake.connector.connect(**conn_params)
        cursor = conn.cursor()
        print("Successfully connected to Snowflake!")
        return conn, cursor
    except Exception as e:
        print("Error connecting to Snowflake:", e)
        return None, None

# Example usage:
# Replace placeholders with your actual Snowflake credentials
conn, cursor = connect_to_snowflake(
    user=config["snowflake"]["user"],
    password=config["snowflake"]["password"],
    account=config["snowflake"]["account"],
    warehouse=config["snowflake"]["warehouse"],
    database=config["snowflake"]["database"],
    schema=config["snowflake"]["schema"]
)

# Once connected, you can execute SQL queries using the cursor
# For example:
if conn and cursor:
    cursor.execute("SELECT * FROM TECREO_DEV.TECH_POC.sud_test_tbl")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Don't forget to close the connection when done
if conn:
    conn.close()


