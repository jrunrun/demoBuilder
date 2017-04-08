import pandas as pd
import datetime as dt
import numpy as np
import random
import math
import time
import locale

print "Demo data exploder starting..."

# Start stopwatch
startTime = time.clock()
# Date and Time stamp for output file
dateTimeStamp = time.strftime("%Y%m%d_%H%M")
#time stamp for file name
outputCSV = dateTimeStamp + '_' + 'DemoData' + ".csv"

#Read in 'Inpatient' and 'Lab Results' data
file1 = '/Users/jcraycraft/Dropbox/Work/PreSales/Marketing/2017_HIMSS/DiabetesReAdmitDemo/Inpatient Data (RMTD) Extract.csv'
file2 = '/Users/jcraycraft/Dropbox/Work/PreSales/Marketing/2017_HIMSS/DiabetesReAdmitDemo/HCPyDiabetesClinical_excludeNone.csv'
#file3 = '/Users/jcraycraft/Dropbox/Work/PreSales/Marketing/2017_HIMSS/DiabetesReAdmitDemo/superstore.csv'
# Read CSV into dataframe (two files)
df1 = pd.read_csv(file1, encoding='utf-16', sep='\t', error_bad_lines=False)
df2 = pd.read_csv(file2)
#df3 = pd.read_csv(file3)

#today's date
today = pd.to_datetime('today')
#date -1460 days equals 4 years from Today
start_dates = today - dt.timedelta(days = 1460)
#create list that includes every day over last 4 years (1460 days)
df_dates3 = pd.date_range(start=start_dates, end=today, freq = 'D').tolist()

#sort all the dates by weekday/year for list of 4 years (1460 days) worth of days
weekdays = [0,1,2,3,4,5,6]
years = [2013,2014,2015,2016,2017]
datesByWeekday = []
final = []
datesByYearAndWeekday = []
for idx, year in enumerate(years):
    result = filter(lambda x: x.year == year, df_dates3)
    for day in weekdays:
        result1 = filter(lambda x: x.weekday()==day, result)
        datesByYearAndWeekday.append(result1)
    final.append(datesByYearAndWeekday) 

#manually set indices for each weekday/year combo
indy_dict = {'Mon':[0,7,14,21,28],'Tues':[1,8,15,22,29],'Wed':[2,9,16,23,30],'Thur':[3,10,17,24,31],'Fri':[4,11,18,25,32],'Sat':[5,12,19,26,33],'Sun':[6,13,20,27,34]}
avgVar_dict = {'Mon':[260,45],'Tues':[277,41],'Wed':[250,20],'Thur':[230,30],'Fri':[223,35],'Sat':[150,20],'Sun':[145,20]}

#create master list of all possible indices from source (option: row level or ID level of detail)
#row level
#df1_idx = df1.index.values.tolist()
#ID level; specify ID; e.g. 'Uniqueid'
df1_idx = df1['Uniqueid'].unique().tolist()

#YoY growth; for now this is the same across all years; enhance later to vary by year
growth = [[1.0,.03],[1.15,.05],[1.175,.07],[1.20,.09],[1.225,.10]]
#growth[0][0]=1
#growth[0][1]=.03

#function that returns dataframe of random indices (given list "df1_idx") and associated date (given date)
def df_builder(indices,rows,date):
    rows = int(rows)
    df_tmp = pd.DataFrame()
    tmp = random.sample(indices,rows)
    df_tmp['indices'] = tmp
    df_tmp['date'] = date
    return(df_tmp)

#containers
out1=[]
output1=[]
out2=[]
output2=[]

#weekday index cycle
for (k,v), (k2,v2) in zip(avgVar_dict.items(), indy_dict.items()):
    tmp_iterator = v2
    
    #year index cycle
    for idx, tmp_item in enumerate(tmp_iterator): 
        
        tmpDates = final[0][v2[idx]]
        factor = math.pow(growth[1][0],idx)
        n = v[0]
        n = float(n)

        n = n * factor
        tmp_df3 = pd.DataFrame()
        out1 = (df_builder(df1_idx,n,date) for date in tmpDates)

        for out_val in out1:
            output1 = pd.concat(out1)
        out2.append(output1)


    for out_val in out2:
        output2 = pd.concat(out2)

    output2['Uniqueid'] = output2['indices']
    output2 = output2.drop('indices', axis=1)      
    output2.to_csv('2017_04_06_output2_v5.csv', index = False)

df1.to_csv('2017_04_06_df1_v5.csv', index = False)
DemoData = pd.merge(df1, output2, on='Uniqueid', how='inner')

#create quantities for both dist and tail for LOS
#use this for discharge dates
df_rows = len(DemoData)
print("rows: ",df_rows)
df_dist = int(len(DemoData) * 0.8)
print("Normdist: ",df_dist)
df_tail = df_rows - df_dist
print("tail: ",df_tail)



DemoData.to_csv(outputCSV, index = False)

print("------------------------------------------------")
print("------------------------------------------------")
print "Demo data exploder finished..."

# Output elapsed time
print "Elapsed time:", locale.format("%.2f", time.clock() - startTime), "seconds"
print("------------------------------------------------")
print("------------------------------------------------")















