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

#Read in 'Inpatient' and 'Lab Results' data
file1 = '/Users/jcraycraft/Dropbox/Work/PreSales/Marketing/2017_HIMSS/DiabetesReAdmitDemo/DemoData/Inpatient Data (RMTD) Extract.csv'
file2 = '/Users/jcraycraft/Dropbox/Work/PreSales/Marketing/2017_HIMSS/DiabetesReAdmitDemo/DemoData/HCPyDiabetesClinical_excludeNone.csv'
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
#daily volumes + variability by weekday
avgVar_dict = {'Mon':[260,45],'Tues':[277,41],'Wed':[250,20],'Thur':[230,30],'Fri':[223,35],'Sat':[150,20],'Sun':[145,20]}

#create master list of all possible indices from source (option: row level or ID level of detail)
    #row level
#df1_idx = df1.index.values.tolist()
    #ID level; specify ID; e.g. 'Uniqueid'
df1_idx = df1['Uniqueid'].unique().tolist()

#YoY growth; for now this is the same across all years; enhance later to vary by year
growth = [[1.0,.03],[1.15,.05],[1.175,.07],[1.20,.09],[1.225,.10]]

#function that returns dataframe of random indices (given list "df1_idx") and associated date (given date)
def df_builder(indices,rows,date):
    rows = int(rows)
    df_tmp = pd.DataFrame()
    tmp = random.sample(indices,rows)
    df_tmp['indices'] = tmp
    df_tmp['Admit_DT'] = date
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
print("total rows: ",df_rows)
df_dist = int(len(DemoData) * 0.8)
print("Normdist: ",df_dist)
df_tail = df_rows - df_dist
print("tail: ",df_tail)

#two distributions for discharge dates so the LOS bins are realistic

total = len(DemoData)

N1 = int(len(DemoData) * 0.8)
N2 = total - N1

#20% of population have higher LOS with greater variability
mu1, sigma1 = 150, 80 # mean and standard deviation
tmp_n1 = np.random.normal(mu1, sigma1, N2)

#80% of population have pretty similar LOS
mu2, sigma2 = 0, 1 # mean and standard deviation
tmp_n2 = np.random.normal(mu2, sigma2, N1)

df_a = pd.DataFrame()
df_a['a'] = tmp_n1
df_a['a'] = abs(df_a['a'])
#comment out below line if you want some LOS=0 days
df_a['a'] = df_a['a']+1
df_a['a'] = df_a['a'].astype(int)
a_list = df_a['a'].tolist()

df_b = pd.DataFrame()
df_b['b'] = tmp_n2
df_b['b'] = abs(df_b['b'])
df_b['b'] = df_b['b']*15
#comment out below line if you want some LOS=0 days
df_b['b'] = df_b['b']+1
df_b['b'] = df_b['b'].astype(int)
b_list = df_b['b'].tolist()

total_list = a_list + b_list

DemoData['delta'] = total_list

DemoData['Disch_DT'] = DemoData['Admit_DT'] + DemoData['delta'].map(dt.timedelta)
DemoData = DemoData.drop('delta', axis=1)

#ENHANCE THIS LATER TO REDUCE NUMBER OF NULLS; MAYBE THIS WOULD BE REALISTIC DATA THOUGH; 14K 'Disch_DT' NULLS CURRENTLY
#clear out any discharges beyond current date
DemoData.ix[DemoData.Disch_DT >= today,'Disch_DT'] = np.NaN


#ENHANCE THIS LATER FOR TRUE READMITS
#create unique MRN for every row; if you want true reAdmits adjust total to <total
mrn = []
mrn = random.sample(range(1000000, 9999999), total)
DemoData['MRN'] = mrn

#create list of unique diabetes releated diagnosis by searching 'DRG Text' column
uniqueDiabetes2 = DemoData[DemoData['DRG Text'].str.contains('DIABETES')==True]['DRG Text'].tolist()
#create list of unique months
DemoData['Admit_month'] = DemoData['Admit_DT'].dt.month
months = DemoData['Admit_month'].unique().tolist()

#create diabetes patients @ specified % of population on monthly basis
for month in months:
    #random percent between 6% and 9%
    test_frac = random.uniform(.06,.09)
    indices = DemoData[DemoData['Admit_month']==month].sample(frac = test_frac).index.tolist()
    for ind in indices:
        DemoData.loc[DemoData.index==ind,'DRG Text']=random.choice(uniqueDiabetes2)
        
#remove legacy fields
fields = ['Uniqueid','From Date','To Date','Length of Stay','Unique ID Join','To Day','Zip Lon','Zip Lat','Miles From Provider']
DemoData = DemoData.drop(fields, axis=1)


uniqueDiabetes22 = DemoData[DemoData['DRG Text'].str.contains('DIABETES')==True]['MRN'].tolist() 


#Create list of indeces filtered where Admit date is >10 days old, but <90 days
start = today - dt.timedelta(days = 90)
end = today - dt.timedelta(days = 10)
#index_tmp = rawDF1[(rawDF1['Admit']>=start)&(rawDF1['Admit']<end)].index.tolist()
ID_tmp = DemoData[(DemoData['Admit_DT']>=start)&(DemoData['Admit_DT']<end)]['MRN'].tolist()

# **DO IT BASED OFF ENCOUNTERID**
# **MAKE SURE 987 OVER LAST QTR IS NOT TOO MANY DIABETES PATIENTS**
#return set with ID's common to both <90days and DRG=diabetes
x=set(uniqueDiabetes22).intersection(ID_tmp)

#ENHANCE TO DETERMINE # BASED OFF LENGTH OF LABS FILE DF
#randomly select 148 OR 987 indices
x_1 = random.sample(x,987)
len(x_1)

#Give it same name for Tableau "smart" join
df2['MRN']=pd.Series(x_1)

# Date and Time stamp for output file
dateTimeStamp = time.strftime("%Y%m%d_%H%M")

#output file names, with time stamp for file name
outputCSV1 = dateTimeStamp + '_' + 'InpatientData' + ".csv"
outputCSV2 = dateTimeStamp + '_' + 'LabsData' + ".csv"

#write csv outputs
df2.to_csv(outputCSV2, index = False)
DemoData.to_csv(outputCSV1, index = False)


print("------------------------------------------------")
print("------------------------------------------------")
print "Demo data exploder finished..."

# Output elapsed time
print "Elapsed time:", locale.format("%.2f", time.clock() - startTime), "seconds"
print("------------------------------------------------")
print("------------------------------------------------")















