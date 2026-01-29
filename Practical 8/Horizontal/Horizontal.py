import pandas as pd
import sqlite3 as sq

# Data Warehouse Connection
conn1 = sq.connect("datawarehouse.db")

# Data Mart Connection
conn2 = sq.connect("datamart.db")

# Load Full Table
sTable = "Dim-BMI"
print("Loading :", sTable)

sSQL = "SELECT * FROM [Dim-BMI];"
PersonFrame0 = pd.read_sql_query(sSQL, conn1)

# Horizontal Selection
sSQL = """
SELECT PersonID,
       Height,
       Weight,
       bmi,
       Indicator
FROM [Dim-BMI]
WHERE Height > 1.5
AND Indicator = 1
ORDER BY Height, Weight;
"""

PersonFrame1 = pd.read_sql_query(sSQL, conn1)

# Set Index
DimPersonIndex = PersonFrame1.set_index("PersonID")

# Store in Data Mart
sTable = "Dim-BMI-Horizontal"
print("Storing :", sTable)

DimPersonIndex.to_sql(sTable, conn2, if_exists="replace")

# Load Result
PersonFrame2 = pd.read_sql_query(
    "SELECT * FROM [Dim-BMI-Horizontal];", conn2
)

# Output Statistics
print("Full Data Set (Rows):", PersonFrame0.shape[0])
print("Full Data Set (Columns):", PersonFrame0.shape[1])
print("Horizontal Data Set (Rows):", PersonFrame2.shape[0])
print("Horizontal Data Set (Columns):", PersonFrame2.shape[1])

conn1.close()
conn2.close()
