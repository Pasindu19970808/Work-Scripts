import pandas as pd
import re

df = pd.read_csv(r'Recommendations-CSV-file_2020-08-31 (1).csv')
df1 = pd.read_excel(r'NodeNo.xlsx', header = None)
df1.rename(columns = {0: 'HAZ360',1 : 'Actual'}, inplace = True)
hazvsactual = dict()
haznumber = df1['HAZ360'].tolist()
actualnumber = df1['Actual'].tolist()

for i in range(0,len(haznumber)):
    hazvsactual[haznumber[i]] = actualnumber[i] 
df.dropna(inplace = True)
usedplaces = df['Place(s) Used'].tolist()
usedplaces

placeusedlist = list()
for i in range(0,len(usedplaces)):
    #test = str(re.findall(r'\bNode Id: \d+ \[Consequence Id: \d+\.\d+\.\d+\]',usedplaces[i]))[1:-1]
    test = re.findall(r'\bNode Id: \d+ \[Consequence Id: \d+\.\d+\.\d+\]',usedplaces[i])
    test2 = list()
    for j in range(0,len(test)):
        test2.append(test[j].replace(re.findall(r'\d+|$',test[j])[0],str(hazvsactual[int(re.findall(r'\d+|$',test[j])[0])])))
    test2 = str(test2)[1:-1]
    test2 = test2.replace(',','\n')
    df['Place(s) Used'].iloc[i] = test2.replace("'","")