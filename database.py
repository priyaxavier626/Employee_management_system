import sqlite3

# Connect to the database
conn = sqlite3.connect("employee.db")

# Create a cursor
cursor = conn.cursor()

# Create Employee table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    department TEXT,
    salary REAL
)
""")

# Save changes
conn.commit()

# Close the connection
conn.close()

print("Database and table created successfully!")  