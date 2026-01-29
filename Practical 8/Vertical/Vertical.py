import pandas as pd
import sqlite3 as sq

# Data Warehouse connection
conn1 = sq.connect("datawarehouse.db")

# Data Mart connection
conn2 = sq.connect("datamart.db")

# Load full dataset
sTable = "Dim-BMI"
print("Loading :", sTable)

sSQL = "SELECT * FROM [Dim-BMI];"
PersonFrame0 = pd.read_sql_query(sSQL, conn1)

# Vertical selection (column-wise)
sSQL = """
SELECT
       Height,
       Weight,
       Indicator
FROM [Dim-BMI];
"""

PersonFrame1 = pd.read_sql_query(sSQL, conn1)

# Set index
DimPersonIndex = PersonFrame1.set_index("Indicator")

# Store vertically organized data
sTable = "Dim-BMI-Vertical"
print("Storing :", sTable)

DimPersonIndex.to_sql(sTable, conn2, if_exists="replace")

# Load result
PersonFrame2 = pd.read_sql_query(
    "SELECT * FROM [Dim-BMI-Vertical];", conn2
)

# Output statistics
print("Full Data Set (Rows):", PersonFrame0.shape[0])
print("Full Data Set (Columns):", PersonFrame0.shape[1])
print("Vertical Data Set (Rows):", PersonFrame2.shape[0])
print("Vertical Data Set (Columns):", PersonFrame2.shape[1])

conn1.close()
conn2.close()
