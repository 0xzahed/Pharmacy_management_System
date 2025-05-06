import mysql.connector

def connect_db():
    """Connect to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",        
            user="root",             
            password="", 
            database="dbpharma",      
            port=3307                 
        )
        return conn
    except mysql.connector.Error as e:
        raise Exception(f"Database connection failed: {str(e)}")
