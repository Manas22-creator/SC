import sys
import os
import pandas as pd
import matplotlib as ml
from matplotlib import pyplot as plt

data = [
    ['London', 29.2, 17.4],
    ['Glasgow', 18.8, 11.3],
    ['Cape Town', 15.3, 9.0],
    ['Houston', 22.0, 7.8],
    ['Perth', 18.0, 23.7],
    ['San Francisco', 11.4, 33.3]
]

os_new = pd.DataFrame(data)

pd.Index(
    ['Item', 'Value', 'Value Percent', 'Conversions', 'Conversion Percent',
     'URL', 'Stats URL'],
    dtype='object'
)

os_new.rename(columns={0: "Warehouse Location"}, inplace=True)
os_new.rename(columns={1: "Profit 2016"}, inplace=True)
os_new.rename(columns={2: "Profit 2017"}, inplace=True)

explode = (0, 0.2, 0, 0, 0, 0.1)
labels = os_new['Warehouse Location']
colors_mine = [
    'yellowgreen', 'gold', 'lightskyblue',
    'lightcoral', 'lightcyan', 'lightblue'
]

os_new.plot(
    figsize=(10, 10),
    kind="pie",
    y="Profit 2017",
    autopct='%.2f%%',
    shadow=True,
    explode=explode,
    legend=False,
    colors=colors_mine,
    labels=labels,
    fontsize=20
)

sPicNameOut1 = 'F:/M.Sc IT Practical/Data Science Practicals/Practical 9/pie_explode.png'
plt.savefig(sPicNameOut1, dpi=600)
plt.show()

os_new.iloc[:5].plot(
    figsize=(10, 10),
    kind='line',
    x='Warehouse Location',
    y=['Profit 2016', 'Profit 2017']
)
plt.show()

os_new.iloc[:5].plot(
    figsize=(10, 10),
    kind='bar',
    x='Warehouse Location',
    y=['Profit 2016', 'Profit 2017']
)
plt.show()

os_new.iloc[:5].plot(
    figsize=(10, 10),
    kind='barh',
    x='Warehouse Location',
    y=['Profit 2016', 'Profit 2017']
)
plt.show()

os_new.iloc[:5].plot(
    figsize=(10, 10),
    kind='area',
    x='Warehouse Location',
    y=['Profit 2016', 'Profit 2017'],
    stacked=False
)
plt.show()

os_new.iloc[:5].plot(
    figsize=(10, 10),
    kind='scatter',
    x='Profit 2016',
    y='Profit 2017',
    color='DarkBlue',
    marker='D'
)
plt.show()

os_new.iloc[:5].plot(
    figsize=(13, 10),
    kind='hexbin',
    x='Profit 2016',
    y='Profit 2017',
    gridsize=25
)
plt.show()
