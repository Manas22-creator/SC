import sqlite3 as sq
import pandas as pd
import uuid

# -------------------- CONFIG --------------------
basePath = 'F:/M.Sc IT Practical/Data Science Practicals/Practical 7'

datavault_path = basePath + '/datavault.db'
vermeulen_path = basePath + '/Vermeulen.db'
datawarehouse_path = basePath + '/datawarehouse.db'

# Suppress pandas warnings
pd.options.mode.chained_assignment = None

# -------------------- CONNECT --------------------
conn_dv = sq.connect(datavault_path)
conn_vm = sq.connect(vermeulen_path)
conn_dw = sq.connect(datawarehouse_path)

# -------------------- UTILITY: FIND TABLE --------------------
def find_table(conn, search_name):
    """
    Find table in SQLite database ignoring case and replacing -/_.
    Returns None if table not found.
    """
    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
    tables_list = tables['name'].tolist()
    search_norm = search_name.lower().replace('-', '_')
    for t in tables_list:
        if t.lower().replace('-', '_') == search_norm:
            return t
    return None

# -------------------- DETECT TABLES --------------------
time_table_name = find_table(conn_dv, "Hub-Time-Gunnarsson")
person_table_name = find_table(conn_dv, "Hub-Person-Gunnarsson")

if not time_table_name:
    print("⚠️ Warning: Hub-Time table not found in datavault.db. Time Dimension will be skipped.")
if not person_table_name:
    print("⚠️ Warning: Hub-Person table not found in datavault.db. Person Dimension will be skipped.")

# -------------------- TIME DIMENSION --------------------
if time_table_name:
    print('\n#################################')
    print('Time Dimension')
    print('#################################\n')

    # Read DateTime values
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
    print('\nStoring Time Dimension in Vermeulen.db and datawarehouse.db')
    DimTimeIndex.to_sql(sTable, conn_vm, if_exists="replace", index=True)
    DimTimeIndex.to_sql(sTable, conn_dw, if_exists="replace", index=True)

# -------------------- PERSON DIMENSION --------------------
if person_table_name:
    print('\n#################################')
    print('Person Dimension')
    print('#################################\n')

    # Read Person data (using DateTimeValue as BirthDateKey)
    sSQL = f"""
    SELECT 
        FirstName,
        LastName,
        DateTimeValue
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
        LastName = str(PersonData.iloc[i]['LastName'])
        BirthDateKey = str(PersonData.iloc[i]['DateTimeValue'])
        IDPersonNumber = str(uuid.uuid4())

        PersonRow = {
            'PersonID': IDPersonNumber,
            'FirstName': FirstName,
            'SecondName': '',  # original logic clears SecondName
            'LastName': LastName,
            'Zone': 'UTC',
            'BirthDate': BirthDateKey
        }

        PersonFrame = pd.concat([PersonFrame, pd.DataFrame([PersonRow])], ignore_index=True)

    DimPersonIndex = PersonFrame.set_index('PersonID', inplace=False)
    print(DimPersonIndex)

    # Store in databases
    sTable = 'Dim-Person'
    print('\nStoring Person Dimension in Vermeulen.db and datawarehouse.db')
    DimPersonIndex.to_sql(sTable, conn_vm, if_exists="replace", index=True)
    DimPersonIndex.to_sql(sTable, conn_dw, if_exists="replace", index=True)

print('\n✅ Sun Model Transformation Completed Successfully!')
