import sqlite3

# Connect to Data Warehouse
conn1 = sqlite3.connect("datawarehouse.db")
cur1 = conn1.cursor()

# Create source table
cur1.execute("""
CREATE TABLE IF NOT EXISTS [Dim-BMI] (
    PersonID INTEGER PRIMARY KEY,
    Height REAL,
    Weight REAL,
    bmi REAL,
    Indicator INTEGER
)
""")

# Clear old data (exam safe)
cur1.execute("DELETE FROM [Dim-BMI];")

# Insert sample data
cur1.executemany("""
INSERT INTO [Dim-BMI] VALUES (?, ?, ?, ?, ?)
""", [
    (1, 1.6, 60, 23.4, 1),
    (2, 1.4, 55, 28.0, 0),
    (3, 1.7, 70, 24.2, 1),
    (4, 1.8, 90, 27.8, 1),
    (5, 1.5, 48, 21.3, 0),
    (6, 1.65, 65, 23.9, 1)
])

conn1.commit()
conn1.close()

# Create Data Mart
conn2 = sqlite3.connect("datamart.db")
conn2.close()

print("Databases and tables created successfully.")
