# test_database.py
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
load_dotenv("connection.env")


load_dotenv()

def test_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT', 3306)
        )
        
        if connection.is_connected():
            print("✅ Successfully connected to MySQL database!")
            
            # Test creating the table
            cursor = connection.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                test_value VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            print("✅ Test table created successfully!")
            
            cursor.close()
            connection.close()
            print("✅ Connection closed properly!")
            
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check if MySQL service is running")
        print("2. Verify database name, username, and password in .env file")
        print("3. Ensure user has proper privileges")
        print("4. Check if MySQL is listening on port 3306")

if __name__ == "__main__":
    test_connection()