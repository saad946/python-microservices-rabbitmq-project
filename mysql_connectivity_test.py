import mysql.connector
from mysql.connector import Error

try:
    # Establish a connection to the MySQL server
    connection = mysql.connector.connect(
        host='localhost',  # Server address
        user='auth_user',  # Username
        password='admin321',  # Password
        database='auth',  # Database name
        port=3306  # Port number
    )

    if connection.is_connected():
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Execute a query to confirm connection
        cursor.execute("SELECT DATABASE()")

        # Fetch and print the result
        database_name = cursor.fetchone()
        print(f"Connected to database: {database_name[0]}")

except Error as e:
    print(f"Error while connecting to MySQL: {e}")

finally:
    if 'cursor' in locals():
        # Clean up cursor
        cursor.close()
    if 'connection' in locals() and connection.is_connected():
        # Clean up connection
        connection.close()
        print("MySQL connection is closed")
