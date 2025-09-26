import sqlite3
from typing import Dict, List, Tuple

def get_database_schema(db_path: str) -> Dict[str, List[Tuple[str, str]]]:
    """
    Analyze database schema and return table structures
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema = {}
    for table in tables:
        table_name = table[0]
        # Get column information
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        schema[table_name] = [(col[1], col[2]) for col in columns]  # name, type
    
    conn.close()
    return schema

def format_schema_for_prompt(schema: Dict[str, List[Tuple[str, str]]]) -> str:
    """
    Format schema information for the prompt
    """
    schema_text = "Database Schema:\n"
    for table, columns in schema.items():
        schema_text += f"\nTable: {table}\n"
        schema_text += "Columns:\n"
        for col_name, col_type in columns:
            schema_text += f"  - {col_name} ({col_type})\n"
    return schema_text