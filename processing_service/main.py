from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI(title="Processing Microservice")

# Database connection configuration for Docker
DB_HOST = "db"  # Changed from localhost to "db" for Docker network
DB_NAME = "market_data_db"
DB_USER = "postgres"
DB_PASSWORD = "S@4508PShib#" 
DB_PORT = "5432"

class MarketData(BaseModel):
    raw_data: str

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def init_db():
    """Ensure the database table exists, waiting for DB to boot if necessary."""
    max_retries = 5
    for i in range(max_retries):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS market_features (
                        id SERIAL PRIMARY KEY,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        original_feed VARCHAR(255) NOT NULL,
                        trading_signal VARCHAR(10) NOT NULL,
                        confidence_score FLOAT NOT NULL
                    );
                """)
                conn.commit()
                print("Database table verified/created successfully.")
                cursor.close()
                conn.close()
                return  # Exit the loop once successful
            except Exception as e:
                print(f"Failed to initialize table: {e}")
        
        print(f"Database not ready yet, retrying in 3 seconds... ({i+1}/{max_retries})")
        time.sleep(3)

# Run this once when the microservice boots up
init_db()

@app.post("/process")
async def process_data(data: MarketData):
    raw_value = data.raw_data
    
    # Simulated Feature Engineering
    processed_feature = {
        "original_feed": raw_value,
        "trading_signal": "BUY",
        "confidence_score": 0.85
    }
    
    # Store in PostgreSQL
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
        
    try:
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO market_features (original_feed, trading_signal, confidence_score)
            VALUES (%s, %s, %s) RETURNING id, timestamp;
        """
        cursor.execute(insert_query, (
            processed_feature["original_feed"], 
            processed_feature["trading_signal"], 
            processed_feature["confidence_score"]
        ))
        
        # Fetch the generated ID and timestamp
        inserted_row = cursor.fetchone()
        conn.commit()
        
        processed_feature["db_id"] = inserted_row[0]
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    
    return {"status": "success", "features": processed_feature}