import sys 
import os 
import pandas as pd 
sInputFile = "Good-or-Bad.csv" 
sOutputFile="Good-orBaad-01.csv" 
RawData=pd.read_csv("C:/Users/vi/Desktop/M.Sc IT Practical/good-or-bad.csv",header=0) 
print(RawData) 
print("Data Profile") 
print("Rows: ",RawData.shape[0]) 
print("Colunms: ",RawData.shape[1]) 
TestData=RawData.fillna(RawData.max()) 
print(TestData) 
print("Data Profile") 
print("Rows: ",RawData.shape[0]) 
print("Colunms: ",RawData.shape[1]) 
TestData.to_csv("C:/Users/vi/Desktop/M.Sc IT Practical/good-or-bad-01.csv",index="False") 
print("Done")
