import pandas as pd 
from datetime import datetime 
sInputFileName='F:/M.Sc IT Practical/M.Sc IT Practical/Practical 3/Country_Code.csv' 
InputData=pd.read_csv(sInputFileName,encoding="latin-1") 
print('Input Data Values ===================================') 
print(InputData) 
ProcessData=InputData 
# Remove columns ISO-2-Code and ISO-3-CODE 
ProcessData.drop('ISO-2-CODE', axis=1,inplace=True) 
ProcessData.drop('ISO-3-Code', axis=1,inplace=True) 
now=datetime.now() 
print("now = ",now) 
dt_string=now.strftime("%d/%m/%y %H:%M:%S") 
print("Date and Time= ",dt_string) 
f=open('F:/M.Sc IT Practical/M.Sc IT Practical/Practical 3/Country_Code_Log.txt',"a") 
f.write("Delete column activity recorded at ") 
f.write(dt_string) 
f.close() 
# Rename Country and ISO-M49 
ProcessData.rename(columns={'Country': 'CountryName'}, inplace=True) 
ProcessData.rename(columns={'ISO-M49': 'CountryNumber'}, inplace=True) 
# Set new Index 
ProcessData.set_index('CountryNumber', inplace=True) 
 
# Sort data by CurrencyNumber 
ProcessData.sort_values('CountryName', axis=0, ascending=False, inplace=True) 
print('Process Data Values =================================') 
print(ProcessData) 
OutputData=ProcessData 
sOutputFileName='F:/M.Sc IT Practical/M.Sc IT Practical/Practical 3/HORUSCSV-Country.csv' 
OutputData.to_csv(sOutputFileName, index = False) 
print('CSV to HORUS - Done')
