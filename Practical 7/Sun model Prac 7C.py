import sqlite3 as sq
import pandas as pd
import uuid
import os

# -------------------- CONFIG --------------------
# Paths to databases
datavault_path = 'F:/M.Sc IT Practical/Data Science Practicals/Practical 7/datavault.db'
vermeulen_path = 'F:/M.Sc IT Practical/Data Science Practicals/Practical 7/Vermeulen.db'
datawarehouse_path = 'F:/M.Sc IT Practical/Data Science Practicals/Practical 7/datawarehouse.db'

# Suppress chained assignment warnings
pd.options.mode.chained_assignment = None

# -------------------- CONNECT --------------------
conn_dv = sq.connect(datavault_path)
conn_vm = sq.connect(vermeulen_path)
conn_dw = sq.connect(datawarehouse_path)

# -------------------- UTILITY: FIND TABLE --------------------
def find_table(conn, search_name):
    """Find table in SQLite database ignoring case and replacing -/_"""
    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
    tables_list = tables['name'].tolist()
    search_norm = search_name.lower().replace('-', '_')
    for t in tables_list:
        if t.lower().replace('-', '_') == search_norm:
            return t
    return None

# -------------------- CHECK TABLES --------------------
time_table_name = find_table(conn_dv, "Hub-Time-Gunnarsson")
person_table_name = find_table(conn_dv, "Hub-Person")

if not time_table_name:
    print("⚠️ Warning: No table found matching 'Hub-Time-Gunnarsson' in datavault.db. Time Dimension will be skipped.")
if not person_table_name:
    print("⚠️ Warning: No table found matching 'Hub-Person' in datavault.db. Person Dimension will be skipped.")

# -------------------- TIME DIMENSION --------------------
if time_table_name:
    print('\n#################################')
    print('Time Dimension')
    print('#################################\n')

    sSQL = f"SELECT DateTimeValue FROM `{time_table_name}`;"
    DateDataRaw = pd.read_sql_query(sSQL, conn_dv)
    DateData = DateDataRaw.head(1000)
    print(DateData)

    TimeFrame = pd.DataFrame()
    t = 0
    mt = DateData.shape[0]

    for i in range(mt):
        BirthZoneList = ('Atlantic/Reykjavik', 'Europe/London', 'UCT')
        for _ in BirthZoneList:
            t += 1
            print(t, mt * 3)

            BirthDateZoneStr = DateData.iloc[i]['DateTimeValue']
            BirthDateLocal = DateData.iloc[i]['DateTimeValue']
            BirthZone = 'UCT'

            IDTimeNumber = str(uuid.uuid4())
            TimeRow = {
                'TimeID': IDTimeNumber,
                'UTCDate': str(BirthDateZoneStr),
                'LocalTime': str(BirthDateLocal),
                'TimeZone': BirthZone
            }
            TimeFrame = pd.concat([TimeFrame, pd.DataFrame([TimeRow])], ignore_index=True)

    DimTimeIndex = TimeFrame.set_index('TimeID', inplace=False)

    # Store in databases
    sTable = 'Dim-Time'
    print('\n#################################')
    print('Storing Time Dimension in Vermeulen.db and datawarehouse.db')
    print('Table:', sTable)
    print('#################################\n')

    DimTimeIndex.to_sql(sTable, conn_vm, if_exists="replace", index=True)
    DimTimeIndex.to_sql(sTable, conn_dw, if_exists="replace", index=True)

# -------------------- PERSON DIMENSION --------------------
if person_table_name:
    print('\n#################################')
    print('Dimension Person')
    print('#################################\n')

    sSQL = f"""
    SELECT 
        FirstName,
        SecondName,
        LastName,
        BirthDateKey
    FROM `{person_table_name}`;
    """
    PersonDataRaw = pd.read_sql_query(sSQL, conn_dv)
    PersonData = PersonDataRaw.head(1000)

    PersonFrame = pd.DataFrame()
    t = 0
    mt = PersonData.shape[0]

    for i in range(mt):
        t += 1
        print(t, mt)

        FirstName = str(PersonData.iloc[i]['FirstName'])
        SecondName = str(PersonData.iloc[i]['SecondName'])
        if len(SecondName) > 0:
            SecondName = ""
        LastName = str(PersonData.iloc[i]['LastName'])
        BirthDateKey = str(PersonData.iloc[i]['BirthDateKey'])
        IDPersonNumber = str(uuid.uuid4())

        PersonRow = {
            'PersonID': IDPersonNumber,
            'FirstName': FirstName,
            'SecondName': SecondName,
            'LastName': LastName,
            'Zone': 'UTC',
            'BirthDate': BirthDateKey
        }

        PersonFrame = pd.concat([PersonFrame, pd.DataFrame([PersonRow])], ignore_index=True)

    DimPersonIndex = PersonFrame.set_index('PersonID', inplace=False)
    print(DimPersonIndex)

    # Store in databases
    sTable = 'Dim-Person'
    print('\n#################################')
    print('Storing Person Dimension in Vermeulen.db and datawarehouse.db')
    print('Table:', sTable)
    print('#################################\n')
    DimPersonIndex.to_sql(sTable, conn_vm, if_exists="replace", index=True)
    DimPersonIndex.to_sql(sTable, conn_dw, if_exists="replace", index=True)

print('\n✅ Process Completed Successfully!')
