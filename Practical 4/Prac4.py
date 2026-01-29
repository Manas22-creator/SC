import sys 
import os 
import sqlite3 as sq 
import pandas as pd 
 
sDatabaseName="F:/M.Sc IT Practical/M.Sc IT Practical DS/Practical 4/project.db" 
conn = sq.connect(sDatabaseName) 
sFileName='IP_DATA_ALL.csv'
print('Loading :',sFileName) 
IP_DATA_ALL=pd.read_csv(sFileName,header=0,low_memory=False, encoding="latin-1") 
 

sTable='IP_DATA_ALL' 
 
print('Storing :',sDatabaseName,' Table:',sTable) 
IP_DATA_ALL.to_sql(sTable, conn, if_exists="replace",index=False) 
 
print('Loading :',sDatabaseName,' Table:',sTable) 
TestData=pd.read_sql_query("select * from IP_DATA_ALL;", conn) 
 
print('## Data Values')   
print(TestData) 
print('## Data Profile')  
print('Rows :',TestData.shape[0]) 
print('Columns :',TestData.shape[1]) 
print('### Done!! ')

conn.close()
