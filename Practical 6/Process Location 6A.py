import sys
import os
import pandas as pd
import sqlite3 as sq
import uuid

Base = 'F:/M.Sc IT Practical/Data Science Practicals/Practical 6'
print('Working Base :', Base, ' using ', sys.platform)

Company = '01-Vermeulen'

sDataBaseDir = Base + '/' + Company + '/03-Process/SQLite'
os.makedirs(sDataBaseDir, exist_ok=True)

sDatabaseName = sDataBaseDir + '/Vermeulen.db'
conn1 = sq.connect(sDatabaseName)

t = 0

# 🔽 REDUCED RANGE (FINITE & SAFE)
for Longitude in range(-180, -120, 10):
    for Latitude in range(-90, -30, 10):
        t += 1
        IDNumber = str(uuid.uuid4())

        LocationName = (
            'L' +
            format(int(Longitude * 1000), '+07d') +
            '-' +
            format(int(Latitude * 1000), '+07d')
        )

        print('Create:', t, ':', LocationName)

        LocationLine = [
            ('ObjectBaseKey', ['GPS']),
            ('IDNumber', [IDNumber]),
            ('LocationNumber', [str(t)]),
            ('LocationName', [LocationName]),
            ('Longitude', [Longitude]),
            ('Latitude', [Latitude])
        ]

        if t == 1:
            LocationFrame = pd.DataFrame(dict(LocationLine))
        else:
            LocationRow = pd.DataFrame(dict(LocationLine))
            LocationFrame = pd.concat([LocationFrame, LocationRow])

LocationHubIndex = LocationFrame.set_index(['IDNumber'], inplace=False)

sTable = 'Process-Location'
LocationHubIndex.to_sql(sTable, conn1, if_exists="replace")

conn1.execute("VACUUM;")

print('### Done!! ############################################')
