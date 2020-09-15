#Used to process Hong Kong Observatory weather data into necessary format
import pandas as pd
import numpy as np

data2015 = open(r'SE2015.txt','r').readlines()
data2016 = open(r'SE2016.txt','r').readlines()
data2017 = open(r'SE2017.txt','r').readlines()
data2018 = open(r'SE2018.txt','r').readlines()
data2019 = open(r'SE2019.txt','r').readlines()
datacompile = [data2015,data2016,data2017,data2018,data2019]

headings = data2015[0].split()
yymm = []
ddhh = []
direction = []
speed = []
PASQ = []
for data in datacompile:
    for i in range(1,len(data)):
        temp = data[i].split()
        yymm.append(float(temp[0][2:]))
        ddhh.append(float(temp[1][-2:]))
        direction.append(float(temp[2]))
        speed.append(float(temp[3])/10)
        PASQ.append(float(temp[4])/10)

yymmarray = np.array(yymm).reshape(-1,1)
ddhharray = np.array(ddhh).reshape(-1,1)
directionarray = np.array(direction).reshape(-1,1)
speedarray = np.array(speed).reshape(-1,1)
pasqarray = np.array(PASQ).reshape(-1,1)

dataset = np.concatenate([yymmarray,ddhharray,directionarray,speedarray,pasqarray],axis = 1)

finaldf = pd.DataFrame(data = dataset, columns  = headings)

idx = finaldf[(finaldf['yymm'] == -3276.7) | (finaldf['ddhh'] == -3276.7) | (finaldf['dir'] == -3276.7) | (finaldf['speed'] == -3276.7) | (finaldf['PASQ'] == -3276.7)].index

newdf = finaldf.drop(idx).reset_index(drop = True)

idx1 = newdf[newdf['PASQ'] == 1.5].index
idx2 = newdf[newdf['PASQ'] == 2.5].index
idx3 = newdf[newdf['PASQ'] == 3.5].index
idx4 = newdf[newdf['PASQ'] == 4.5].index
idx5 = newdf[newdf['PASQ'] == 5.5].index
#50:50
#len = 1538
newdf.iloc[idx1[:(int(len(idx1)/2))],4] = 1.0
newdf.iloc[idx1[(int(len(idx1)/2)):],4] = 2.0

newdf.iloc[idx2[:(int(len(idx2)/2))],4] = 2.0
newdf.iloc[idx2[(int(len(idx2)/2)):],4] = 3.0

newdf.iloc[idx3[:(int(len(idx3)/2))],4] = 3.0
newdf.iloc[idx3[(int(len(idx3)/2)):],4] = 4.0

newdf.iloc[idx4[:(int(len(idx4)/2))],4] = 4.0
newdf.iloc[idx4[(int(len(idx4)/2)):],4] = 5.0

newdf.iloc[idx5[:(int(len(idx5)/2))],4] = 5.0
newdf.iloc[idx5[(int(len(idx5)/2)):],4] = 6.0

newdf['Class'] = np.nan

pasqldict = {1:'A',2:'B',3:'C',4 : 'D',5:'E',6:'F'}

for group in pasqldict:
    newdf.loc[newdf['PASQ'] == group,'Class'] = pasqldict[group]

cols = ['speed','Class']

newdf['Weather Class'] = newdf['speed'].astype(str) + '' + newdf['Class']

newdf['Direction Range'] = np.nan

newdf.loc[newdf['dir'] <= 30, 'Direction Range'] = '0 - 30'
newdf.loc[(newdf['dir'] >= 30) & (newdf['dir'] <= 60), 'Direction Range'] = '30 - 60'
newdf.loc[(newdf['dir'] >= 60) & (newdf['dir'] <= 90), 'Direction Range'] = '60 - 90'
newdf.loc[(newdf['dir'] >= 90) & (newdf['dir'] <= 120), 'Direction Range'] = '90 - 120'
newdf.loc[(newdf['dir'] >= 120) & (newdf['dir'] <= 150), 'Direction Range'] = '120 - 150'
newdf.loc[(newdf['dir'] >= 150) & (newdf['dir'] <= 180), 'Direction Range'] = '150 - 180'
newdf.loc[(newdf['dir'] >= 180) & (newdf['dir'] <= 210), 'Direction Range'] = '180 - 210'
newdf.loc[(newdf['dir'] >= 210) & (newdf['dir'] <= 240), 'Direction Range'] = '210 - 240'
newdf.loc[(newdf['dir'] >= 240) & (newdf['dir'] <= 270), 'Direction Range'] = '240 - 270'
newdf.loc[(newdf['dir'] >= 270) & (newdf['dir'] <= 300), 'Direction Range'] = '270 - 300'
newdf.loc[(newdf['dir'] >= 300) & (newdf['dir'] <= 330), 'Direction Range'] = '300 - 330'    
newdf.loc[(newdf['dir'] >= 330) & (newdf['dir'] <= 360), 'Direction Range'] = '330 - 360'

idxdir = newdf[newdf['dir'] == 9999].index
df = newdf.drop(idxdir).reset_index(drop = True)

daydf = df.loc[(df['ddhh'].astype(int) == 7) | (df['ddhh'].astype(int) == 8) | (df['ddhh'].astype(int) == 9) | (df['ddhh'].astype(int) == 10) | (df['ddhh'].astype(int) == 11) |\
                (df['ddhh'].astype(int) == 12) | (df['ddhh'].astype(int) == 13) | (df['ddhh'].astype(int) == 14) | (df['ddhh'].astype(int) == 15) | (df['ddhh'].astype(int) == 16)|\
                (df['ddhh'].astype(int) == 17) | (df['ddhh'].astype(int) == 18)].reset_index(drop = True)

nightdf = df.loc[(df['ddhh'].astype(int) == 1) | (df['ddhh'].astype(int) == 2) | (df['ddhh'].astype(int) == 3) | (df['ddhh'].astype(int) == 4) | (df['ddhh'].astype(int) == 5) |\
                (df['ddhh'].astype(int) == 6) | (df['ddhh'].astype(int) == 19) | (df['ddhh'].astype(int) == 20) | (df['ddhh'].astype(int) == 21) | (df['ddhh'].astype(int) == 22)|\
                (df['ddhh'].astype(int) == 23) | (df['ddhh'].astype(int) == 24)].reset_index(drop = True)

daydf['Cumulative Weather Class'] = np.nan
#3B day time
daydf.loc[((daydf['speed'] >= 0) & (daydf['speed'] <= 4)) & ((daydf['Class'] == 'A') | (daydf['Class'] == 'B')), 'Cumulative Weather Class'] = '3B'
#4C day time 
daydf.loc[((daydf['speed'] > 4) & (daydf['speed'] <= 22)) & ((daydf['Class'] == 'A') | (daydf['Class'] == 'B') | (daydf['Class'] == 'C')), 'Cumulative Weather Class'] = '4C'
daydf.loc[((daydf['speed'] >= 0) & (daydf['speed'] <= 4)) & ((daydf['Class'] == 'C')), 'Cumulative Weather Class'] = '4C'
#1D day time 
daydf.loc[((daydf['speed'] >= 0) & (daydf['speed'] <= 4)) & ((daydf['Class'] == 'D')), 'Cumulative Weather Class'] = '1D'
#7D day time 
daydf.loc[((daydf['speed'] > 4) & (daydf['speed'] <= 22)) & ((daydf['Class'] == 'D') | (daydf['Class'] == 'E') | (daydf['Class'] == 'F')), 'Cumulative Weather Class'] = '7D'
#3E day time 
daydf.loc[((daydf['speed'] >= 0) & (daydf['speed'] <= 4)) & ((daydf['Class'] == 'E')), 'Cumulative Weather Class'] = '3E'
daydf.loc[((daydf['speed'] > 3) & (daydf['speed'] <= 4)) & ((daydf['Class'] == 'F')), 'Cumulative Weather Class'] = '3E'
#1F day time 
daydf.loc[((daydf['speed'] >= 0) & (daydf['speed'] <= 3)) & ((daydf['Class'] == 'F')), 'Cumulative Weather Class'] = '1F'


nightdf['Cumulative Weather Class'] = np.nan
#1B night time
nightdf.loc[((nightdf['speed'] >= 0) & (nightdf['speed'] <= 2)) & ((nightdf['Class'] == 'A') | (nightdf['Class'] == 'B')), 'Cumulative Weather Class'] = '1B'
#4D night time 
nightdf.loc[((nightdf['speed'] > 2) & (nightdf['speed'] <= 3)) & ((nightdf['Class'] == 'A') | (nightdf['Class'] == 'B') | (nightdf['Class'] == 'C')\
             | (nightdf['Class'] == 'D')), 'Cumulative Weather Class'] = '4D'

nightdf.loc[((nightdf['speed'] > 3) & (nightdf['speed'] <= 5)) & ((nightdf['Class'] == 'A') | (nightdf['Class'] == 'B') | (nightdf['Class'] == 'C')\
             | (nightdf['Class'] == 'D') | (nightdf['Class'] == 'E') | (nightdf['Class'] == 'F')), 'Cumulative Weather Class'] = '4D'

nightdf.loc[((nightdf['speed'] >= 0) & (nightdf['speed'] <= 2)) & ((nightdf['Class'] == 'C')), 'Cumulative Weather Class'] = '4D'

#1D night time 
nightdf.loc[((nightdf['speed'] >= 0) & (nightdf['speed'] <= 2)) & ((nightdf['Class'] == 'D')), 'Cumulative Weather Class'] = '1D'

#7D night time 
nightdf.loc[((nightdf['speed'] > 5) & (nightdf['speed'] <= 22)) & ((nightdf['Class'] == 'A') | (nightdf['Class'] == 'B') | (nightdf['Class'] == 'C')\
             | (nightdf['Class'] == 'D') | (nightdf['Class'] == 'E') | (nightdf['Class'] == 'F')), 'Cumulative Weather Class'] = '7D'

#3E night time 
nightdf.loc[((nightdf['speed'] >= 0) & (nightdf['speed'] <= 2)) & ((nightdf['Class'] == 'E')), 'Cumulative Weather Class'] = '3E'
nightdf.loc[((nightdf['speed'] > 2) & (nightdf['speed'] <= 3)) & ((nightdf['Class'] == 'F') | (nightdf['Class'] == 'E')), 'Cumulative Weather Class'] = '3E'

#1F day time 
nightdf.loc[((nightdf['speed'] >= 0) & (nightdf['speed'] <= 2)) & ((nightdf['Class'] == 'F')), 'Cumulative Weather Class'] = '1F'

    
    
    
    
    