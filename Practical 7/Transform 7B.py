import sys
import os
from datetime import datetime
from pytz import timezone
import pandas as pd
import sqlite3 as sq
import uuid

pd.options.mode.chained_assignment = None

# ---------------- DATABASE PATHS ----------------
basePath = 'F:/M.Sc IT Practical/Data Science Practicals/Practical 7'
os.makedirs(basePath, exist_ok=True)

conn1 = sq.connect(basePath + '/Vermeulen.db')
conn2 = sq.connect(basePath + '/datavault.db')
conn3 = sq.connect(basePath + '/datawarehouse.db')

print('\n#################################')
print('Time Category')
print('UTC Time')

BirthDateUTC = datetime(1960, 12, 20, 10, 15, 0)
BirthDateZoneUTC = BirthDateUTC.replace(tzinfo=timezone('UTC'))
BirthDateZoneStr = BirthDateZoneUTC.strftime("%Y-%m-%d %H:%M:%S")
BirthDateZoneUTCStr = BirthDateZoneUTC.strftime(
    "%Y-%m-%d %H:%M:%S (%Z) (%z)"
)

print(BirthDateZoneUTCStr)
print('#################################')

print('Birth Date in Reykjavik :')
BirthZone = 'Atlantic/Reykjavik'
BirthDate = BirthDateZoneUTC.astimezone(timezone(BirthZone))
BirthDateStr = BirthDate.strftime("%Y-%m-%d %H:%M:%S (%Z) (%z)")
BirthDateLocal = BirthDate.strftime("%Y-%m-%d %H:%M:%S")

print(BirthDateStr)
print('#################################')

# ---------------- TIME DATA ----------------
IDZoneNumber = str(uuid.uuid4())
sDateTimeKey = BirthDateZoneStr.replace(' ', '-').replace(':', '-')

TimeLine = {
    'ZoneBaseKey': ['UTC'],
    'IDNumber': [IDZoneNumber],
    'DateTimeKey': [sDateTimeKey],
    'UTCDateTimeValue': [BirthDateZoneUTC],
    'Zone': [BirthZone],
    'DateTimeValue': [BirthDateStr]
}

TimeFrame = pd.DataFrame(TimeLine)

# ---------------- TIME HUB ----------------
TimeHub = TimeFrame[['IDNumber', 'ZoneBaseKey', 'DateTimeKey', 'DateTimeValue']]
TimeHubIndex = TimeHub.set_index('IDNumber')

sTable = 'Hub-Time-Gunnarsson'
TimeHubIndex.to_sql(sTable, conn2, if_exists="replace")

sTable = 'Dim-Time-Gunnarsson'
TimeHubIndex.to_sql(sTable, conn3, if_exists="replace")

# ---------------- TIME SATELLITE ----------------
TimeSatellite = TimeFrame[['IDNumber', 'DateTimeKey', 'Zone', 'DateTimeValue']]
TimeSatelliteIndex = TimeSatellite.set_index('IDNumber')

BirthZoneFix = BirthZone.replace(' ', '-').replace('/', '-')
sTable = 'Satellite-Time-' + BirthZoneFix + '-Gunnarsson'
TimeSatelliteIndex.to_sql(sTable, conn2, if_exists="replace")

sTable = 'Dim-Time-' + BirthZoneFix + '-Gunnarsson'
TimeSatelliteIndex.to_sql(sTable, conn3, if_exists="replace")

# ---------------- PERSON CATEGORY ----------------
print('\n#################################')
print('Person Category')

FirstName = 'abc'
LastName = 'pqr'

print('Name:', FirstName, LastName)
print('Birth Date:', BirthDateLocal)
print('Birth Zone:', BirthZone)
print('UTC Birth Date:', BirthDateZoneStr)
print('#################################')

IDPersonNumber = str(uuid.uuid4())

PersonLine = {
    'IDNumber': [IDPersonNumber],
    'FirstName': [FirstName],
    'LastName': [LastName],
    'Zone': ['UTC'],
    'DateTimeValue': [BirthDateZoneStr]
}

PersonFrame = pd.DataFrame(PersonLine)
PersonHubIndex = PersonFrame.set_index('IDNumber')

sTable = 'Hub-Person-Gunnarsson'
PersonHubIndex.to_sql(sTable, conn2, if_exists="replace")

sTable = 'Dim-Person-Gunnarsson'
PersonHubIndex.to_sql(sTable, conn3, if_exists="replace")

print('\n### Done!! ############################################')
