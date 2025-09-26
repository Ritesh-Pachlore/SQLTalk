import sqlite3

def read_sql_query(sql, db):
    """
    Execute a SQL query and return the results.
    
    Args:
        sql (str): SQL query to execute
        db (str): Path to the SQLite database file
    
    Returns:
        list: Query results as a list of tuples
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()    
    return rows

def init_database(db_path):
    """
    Initialize the database with the STUDENT table if it doesn't exist.
    
    Args:
        db_path (str): Path where the database should be created
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the STUDENT table if it doesn't exist
    table_info = """
    CREATE TABLE IF NOT EXISTS STUDENT(
        NAME VARCHAR(25),
        CLASS VARCHAR(25),
        SECTION VARCHAR(25),
        MARKS INT
    );
    """
    cursor.execute(table_info)
    
    # Check if the table is empty
    cursor.execute("SELECT COUNT(*) FROM STUDENT")
    if cursor.fetchone()[0] == 0:
        # Insert sample data
        sample_data = [
            ('Krish', 'Data Science', 'A', 90),
            ('Sudhanshu', 'Data Science', 'B', 100),
            ('Darius', 'Data Science', 'A', 86),
            ('Vikash', 'DEVOPS', 'A', 50),
            ('Dipesh', 'DEVOPS', 'A', 35)
        ]
        
        cursor.executemany('INSERT INTO STUDENT VALUES (?,?,?,?)', sample_data)
    
    conn.commit()
    conn.close()