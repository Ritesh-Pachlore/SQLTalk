import sqlite3
from typing import List, Tuple, Any
import pandas as pd

def read_sql_query(sql: str, db: str) -> List[Tuple[Any, ...]]:
    """
    Execute SQL query and return results
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        raise e
    finally:
        conn.close()

def get_query_results_with_columns(sql: str, db: str) -> Tuple[List[str], List[Tuple[Any, ...]]]:
    """
    Execute SQL query and return results with column names
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        columns = [description[0] for description in cur.description] if cur.description else []
        rows = cur.fetchall()
        return columns, rows
    except Exception as e:
        raise e
    finally:
        conn.close()

def validate_sql_query(sql: str) -> bool:
    """
    Basic SQL query validation
    """
    # Prevent dangerous operations
    dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE', 'INSERT', 'UPDATE']
    sql_upper = sql.upper()
    
    for keyword in dangerous_keywords:
        if keyword in sql_upper:
            return False
    
    # Ensure it's a SELECT query
    if not sql_upper.strip().startswith('SELECT'):
        return False
    
    return True