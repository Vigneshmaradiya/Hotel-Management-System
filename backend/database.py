import psycopg2
from psycopg2 import pool, Error
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

# Use DATABASE_URL if available (for cloud deployment), otherwise construct from parts
def get_db_connection():
    """Create and return a database connection"""
    try:
        # Check for DATABASE_URL (common in cloud platforms)
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            # Add SSL mode for Supabase/cloud databases if not already in URL
            if 'sslmode=' not in database_url:
                database_url += '?sslmode=require'
            connection = psycopg2.connect(database_url)
        else:
            # Fallback to individual connection parameters
            connection = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=int(os.getenv('DB_PORT', 5432)),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'postgres'),
                database=os.getenv('DB_NAME', 'hotel_management'),
                sslmode='require'
            )
        
        return connection
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        print(f"Connection string (without password): {database_url.split(':')[0] if database_url else 'Using individual params'}")
        return None

def close_db_connection(connection):
    """Close the database connection"""
    if connection and not connection.closed:
        connection.close()
