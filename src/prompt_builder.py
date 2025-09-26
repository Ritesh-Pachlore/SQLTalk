def build_dynamic_prompt(schema_info: str, examples: str = "") -> str:
    """
    Build a comprehensive prompt for SQL generation
    """
    prompt = f"""You are an expert SQL query generator. Convert natural language questions to SQL queries based on the following database schema.

{schema_info}

Important Rules:
1. Generate only valid SQL queries without any markdown formatting or backticks
2. Use proper SQL syntax for the database type
3. Handle case sensitivity appropriately
4. Use appropriate JOIN clauses when querying multiple tables
5. Include proper WHERE clauses for filtering
6. Use aggregate functions (COUNT, SUM, AVG, MAX, MIN) when appropriate
7. Handle NULL values properly
8. Use GROUP BY when using aggregate functions with other columns
9. Use ORDER BY for sorting when requested
10. Use LIMIT for restricting results when asked for "top" or specific number of results

Common Query Patterns:
- For counting: SELECT COUNT(*) FROM table_name
- For all records: SELECT * FROM table_name
- For specific columns: SELECT column1, column2 FROM table_name
- For filtering: SELECT * FROM table_name WHERE condition
- For joining: SELECT * FROM table1 JOIN table2 ON table1.id = table2.id
- For grouping: SELECT column, COUNT(*) FROM table_name GROUP BY column
- For ordering: SELECT * FROM table_name ORDER BY column ASC/DESC
- For distinct values: SELECT DISTINCT column FROM table_name

{examples}

Now convert the following question to SQL:
"""
    return prompt