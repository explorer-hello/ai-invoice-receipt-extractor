import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
load_dotenv("connection.env")


load_dotenv()

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST','localhost'),
            database=os.getenv('DB_NAME','invoice_extractor'),
            user=os.getenv('DB_USER','sunny'),
            password=os.getenv('DB_PASSWORD','M.sunny@13')
        )
        print("connection sucessful")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_database():
    conn = create_connection()
    if conn is None:
        return
    
    try:
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            vendor VARCHAR(255) NOT NULL,
            invoice_date DATE,
            amount DECIMAL(10, 2) NOT NULL,
            tax DECIMAL(10, 2) DEFAULT 0,
            category VARCHAR(50),
            invoice_number VARCHAR(100),
            raw_text TEXT,
            file_name VARCHAR(255),
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        conn.commit()
        print("Database initialized successfully")
        
    except Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def save_invoice_data(invoice_data, filename):
    conn = create_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        
        query = """
        INSERT INTO invoices (vendor, invoice_date, amount, tax, category, invoice_number, raw_text, file_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            invoice_data.get('vendor'),
            invoice_data.get('date'),
            invoice_data.get('amount'),
            invoice_data.get('tax'),
            invoice_data.get('category'),
            invoice_data.get('invoice_number'),
            invoice_data.get('raw_text'),
            filename
        )
        
        cursor.execute(query, values)
        conn.commit()
        return cursor.lastrowid
        
    except Error as e:
        print(f"Error saving invoice data: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_invoices(limit=50, offset=0):
    conn = create_connection()
    if conn is None:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM invoices ORDER BY processed_at DESC LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, offset))
        
        results = cursor.fetchall()
        
        # Convert decimal to float for JSON serialization
        for row in results:
            if row['amount'] is not None:
                row['amount'] = float(row['amount'])
            if row['tax'] is not None:
                row['tax'] = float(row['tax'])
            if row['invoice_date'] is not None:
                row['invoice_date'] = row['invoice_date'].isoformat()
            if row['processed_at'] is not None:
                row['processed_at'] = row['processed_at'].isoformat()
                
        return results
        
    except Error as e:
        print(f"Error fetching invoices: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_invoice_by_id(invoice_id):
    conn = create_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM invoices WHERE id = %s"
        cursor.execute(query, (invoice_id,))
        
        result = cursor.fetchone()
        
        if result:
            # Convert decimal to float for JSON serialization
            if result['amount'] is not None:
                result['amount'] = float(result['amount'])
            if result['tax'] is not None:
                result['tax'] = float(result['tax'])
            if result['invoice_date'] is not None:
                result['invoice_date'] = result['invoice_date'].isoformat()
            if result['processed_at'] is not None:
                result['processed_at'] = result['processed_at'].isoformat()
                
        return result
        
    except Error as e:
        print(f"Error fetching invoice: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Initialize database when module is imported
init_database()