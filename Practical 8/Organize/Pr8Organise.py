 
import sys 
import os 
import pandas as pd 
import networkx as nx 
import matplotlib.pyplot as plt 
pd.options.mode.chained_assignment = None 
sFileName='F:/M.Sc IT Practical/M.Sc IT Practical/Practical 8/Assess-Network-Routing-Company.csv' 
print('Loading :',sFileName) 
CompanyData=pd.read_csv(sFileName,header=0,low_memory=False, encoding="latin-1") 
print(CompanyData.head()) 
print(CompanyData.shape) 
G=nx.Graph() 
for i in range(CompanyData.shape[0]): 
    for j in range(CompanyData.shape[0]): 
        Node0=CompanyData['Company_Country_Name'][i] 
        Node1=CompanyData['Company_Country_Name'][j] 
        if Node0 != Node1: 
            G.add_edge(Node0,Node1) 
for i in range(CompanyData.shape[0]): 
    Node0=CompanyData['Company_Country_Name'][i] 
    Node1=CompanyData['Company_Place_Name'][i] + '('+ CompanyData['Company_Country_Name'][i] + ')' 
    if Node0 != Node1: 
        G.add_edge(Node0,Node1) 
print('Nodes:', G.number_of_nodes())    
print('Edges:', G.number_of_edges())       
sFileName='F:/M.Sc IT Practical/M.Sc IT Practical/Practical 8/Assess-Network-Routing-Company.csv' 
print('Storing :',sFileName) 
#nx.write_gml(G, sFileName)       
sFileName='F:/M.Sc IT Practical/M.Sc IT Practical/Practical 8/Assess-Network-Routing-Company.csv' 
print('Storing Graph Image:',sFileName) 
plt.figure(figsize=(15, 15)) 
pos=nx.spectral_layout(G,dim=2) 
nx.draw_networkx_nodes(G,pos, node_color='k', node_size=10, alpha=0.8) 
nx.draw_networkx_edges(G, pos,edge_color='r', arrows=False, style='dashed') 
nx.draw_networkx_labels(G,pos,font_size=12,font_family='sans-serif',font_color='b') 
plt.axis('off') 
#plt.savefig(sFileName,dpi=600) 
plt.show() 
print('### Done!! #####################')
