import sys
import os
import pandas as pd
import sqlite3 as sq

# ---------------- BASE DIRECTORY (FOLDER ONLY) ----------------
Base = 'F:/M.Sc IT Practical/Data Science Practicals/Practical 6'
print('Working Base :', Base, ' using ', sys.platform)

Company = '01-Vermeulen'

# ---------------- CSV FILE (ACTUAL LOCATION) ----------------
sFileName = Base + '/' + Company + '/Action_Plan.csv'
print('Loading :', sFileName)

# ---------------- DATABASE DIRECTORY ----------------
sDataBaseDir = Base + '/' + Company + '/03-Process/SQLite'
os.makedirs(sDataBaseDir, exist_ok=True)

sDatabaseName = sDataBaseDir + '/Vermeulen.db'
conn1 = sq.connect(sDatabaseName)

# ---------------- LOAD EVENT DATA ----------------
EventRawData = pd.read_csv(
    sFileName,
    header=0,
    low_memory=False,
    encoding="latin-1"
)

EventRawData.index.names = ['EventID']
EventHubIndex = EventRawData

# ---------------- STORE INTO SQLITE ----------------
sTable = 'Process-Event'
print('Storing Table:', sTable)

EventHubIndex.to_sql(sTable, conn1, if_exists="replace")

# ---------------- OPTIMIZE DATABASE ----------------
conn1.execute("VACUUM;")

print('### Done!! ############################################')
