import sys 
import os 
import pandas as pd 
sInputFile = "Good-or-Bad.csv" 
sOutputFile="Good-orBaad-01.csv" 
RawData=pd.read_csv("F:/M.Sc IT Practical/M.Sc IT Practical/Practical 5/Prac5C mean min max/good-or-bad.csv",header=0) 
print(RawData) 
print("Data Profile") 
print("Rows: ",RawData.shape[0]) 
print("Colunms: ",RawData.shape[1]) 
TestData=RawData.fillna(RawData.mean()) 
print(TestData) 
print("Data Profile") 
print("Rows: ",RawData.shape[0]) 
print("Colunms: ",RawData.shape[1]) 
TestData.to_csv("F:/M.Sc IT Practical/M.Sc IT Practical/Practical 5/Prac5C mean min max/good-or-bad-01.csv",index="False") 
print("Done")
