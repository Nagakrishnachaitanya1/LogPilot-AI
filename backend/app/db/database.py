import sqlite3
from datetime import datetime


def create_table():

    connection = sqlite3.connect("logpilot.db")
    try:
        
        cursor = connection.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS incidents(
            id INTEGER PRIMARY KEY,
            log_text TEXT,
            analysis TEXT,
            created_at TEXT
        )""")

        connection.commit()
    
    finally:
        connection.close()


def insert(log_text,analysis):

    connection = sqlite3.connect("logpilot.db")
    
    try:
        cursor = connection.cursor()
            
        cursor.execute(
            """INSERT INTO incidents (log_text, analysis, created_at)
            VALUES (?, ?, ?)""",
            (log_text, analysis, datetime.now().isoformat())
        )

        connection.commit()
    
    finally:
        connection.close()


if __name__ == "__main__":
    create_table()
    log_text = """sqlite3.OperationalError: unable to open database file"""

    analysis = """
        {
            "severity": "high",
            "category": "SQLite Database Connection Error",
            "summary": "The application failed to open the SQLite database file.",
            "confidence": "high"
        } """
    insert(log_text, analysis)