# Database configurations
DATABASE_CONFIGS = {
    "SQLite": {
        "file_extension": ".db",
        "connection_string": "sqlite:///{path}"
    },
    "MySQL": {
        "default_port": 3306,
        "connection_string": "mysql://{user}:{password}@{host}:{port}/{database}"
    },
    "PostgreSQL": {
        "default_port": 5432,
        "connection_string": "postgresql://{user}:{password}@{host}:{port}/{database}"
    }
}

# SQL validation rules
DANGEROUS_KEYWORDS = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE', 'INSERT', 'UPDATE']
ALLOWED_KEYWORDS = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'GROUP BY', 'ORDER BY', 'HAVING', 'LIMIT']