import sqlite3

# Connect to the local database file (it will be created automatically)
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# 1. Create a Sample Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INTEGER
)""")

# 2. Insert Test Data
cursor.executemany("INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)", [
    ("Alice", "Engineering", 95000),
    ("Bob", "Marketing", 75000),
    ("Charlie", "Engineering", 110000),
    ("Diana", "Sales", 85000)
])

# Commit changes and close connection
conn.commit()
conn.close()
print("Database 'company.db' successfully initialized!")
