import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",  # Default XAMPP MySQL user
    "password": "",  # Empty if you haven't set a password
    "database": "portfolio_db"
}


# Function to connect to MySQL
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None
