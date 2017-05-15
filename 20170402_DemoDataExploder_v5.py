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
file1 = '/Users/jcraycraft/Dropbox/Work/PreSales/Marketing/2017_HIMSS/DiabetesReAdmitDemo/DemoData2/Inpatient Data (RMTD) Extract.csv'
file2 = '/Users/jcraycraft/Dropbox/Work/PreSales/Marketing/2017_HIMSS/DiabetesReAdmitDemo/DemoData2/HCPyDiabetesClinical_excludeNone2.csv'

# Read CSV into dataframe (two files)
df1 = pd.read_csv(file1, encoding='utf-16', sep='\t', error_bad_lines=False)
df2 = pd.read_csv(file2)

#arbitrarily lowering charges across board
df1['Total Charges'] = df1['Total Charges'] * 0.75

#grab indices for each type of diabetes
diab_mcc_idx = df1[df1['DRG Text']=='DIABETES W MCC'].index.values.tolist()
diab_cc_idx = df1[df1['DRG Text']=='DIABETES W CC'].index.values.tolist()
diab_idx = df1[df1['DRG Text']=='DIABETES W/O CC/MCC'].index.values.tolist()
diab_all_idx = diab_mcc_idx + diab_cc_idx + diab_idx

#grab Uniqueid's for each type of diabetes
diab_mcc = df1[df1['DRG Text']=='DIABETES W MCC']['Uniqueid'].unique().tolist()
diab_cc = df1[df1['DRG Text']=='DIABETES W CC']['Uniqueid'].unique().tolist()
diab = df1[df1['DRG Text']=='DIABETES W/O CC/MCC']['Uniqueid'].unique().tolist()
diab_all = diab_mcc + diab_cc + diab

#adjust charges for each type of diabetes
#using index as filter
df1.loc[diab_mcc_idx,'Total Charges'] = df1.loc[diab_mcc_idx,'Total Charges']*1.1
df1.loc[diab_cc_idx,'Total Charges'] = df1.loc[diab_cc_idx,'Total Charges']*0.9
df1.loc[diab_idx,'Total Charges'] = df1.loc[diab_idx,'Total Charges']*0.75

#calc LOS from input file
df1['LOS_tmp'] = pd.to_datetime(df1['To Date']) - pd.to_datetime(df1['From Date'])
# +1 to include current day
df1['LOS_tmp'] = df1['LOS_tmp'].dt.days + 1 

#daily unit costs = total charges/LOS
df1['Charge_perDay_tmp'] = df1['Total Charges'] / df1['LOS_tmp']
df1['Charge_perDay_tmp'] = df1['Charge_perDay_tmp'].astype('int')

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

#ENHANCE TO CREATE THIS IN BACKGROUND PRIOR TO ITERATING BELOW
#manually set indices for each weekday/year combo
indy_dict = {'Mon':[0,7,14,21,28],'Tues':[1,8,15,22,29],'Wed':[2,9,16,23,30],'Thur':[3,10,17,24,31],'Fri':[4,11,18,25,32],'Sat':[5,12,19,26,33],'Sun':[6,13,20,27,34]}
#daily volumes + variability by weekday
avgVar_dict = {'Mon':[260,45],'Tues':[277,41],'Wed':[250,20],'Thur':[230,30],'Fri':[223,35],'Sat':[150,20],'Sun':[145,20]}

#create master list of all 'Uniqueid' values; i.e. unique patients
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
    #output2.to_csv('2017_04_06_output2_v5.csv', index = False)

#reset index for 400K+ row dataframe output
output2 = output2.reset_index(drop=True)
#create list of unique months
output2['Admit_month'] = output2['Admit_DT'].dt.month
months = output2['Admit_month'].unique().tolist()

#create diabetes patients @ specified % of population on monthly basis
#using Uniqueid as filter
for month in months:
    #random percent between 6% and 9%
    test_frac = random.uniform(.03,.05)
    indices = output2[output2['Admit_month']==month].sample(frac = test_frac).index.tolist()
    for ind in indices:
        #DemoData.loc[DemoData.index==ind,'DRG Text']=random.choice(uniqueDiabetes2)
        output2.loc[ind,'Uniqueid']=random.choice(diab_all)

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
#return list of disbributions
#input mean (mu) & std deviation (sigma)
def dist_builder(length,mu1,sigma1,mu2,sigma2,base,percent_normal):
    df2 = pd.DataFrame()
    N1 = int(length * percent_normal)
    N2 = length - N1
    tmp_n1 = np.random.normal(mu1, sigma1, N2)
    tmp_n1 = abs(tmp_n1)
    tmp_n2 = np.random.normal(mu2, sigma2, N1)
    tmp_n2 = abs(tmp_n2)

    a = pd.Series(tmp_n1+1)
    a_list = a.astype('int').tolist()

    b = pd.Series((tmp_n2*base)+1)
    b_list = b.astype('int').tolist()

    total_list = a_list + b_list
    return(total_list)

length_df = len(DemoData)
DemoData['delta'] = dist_builder(length_df,17,11,5,2,1,.80)

DemoData['Disch_DT'] = DemoData['Admit_DT'] + DemoData['delta'].map(dt.timedelta)
DemoData = DemoData.drop('delta', axis=1)

#grab indexes for each type of diabetes
diab_mcc = DemoData[DemoData['DRG Text']=='DIABETES W MCC'].index.tolist()
diab_cc = DemoData[DemoData['DRG Text']=='DIABETES W CC'].index.tolist()
diab = DemoData[DemoData['DRG Text']=='DIABETES W/O CC/MCC'].index.tolist()

#create distributions for LOS
DemoData.loc[diab_mcc,'delta_diab_mcc'] = dist_builder(len(diab_mcc),30,18,12,8,1,.80)
DemoData.loc[diab_cc,'delta_diab_cc'] = dist_builder(len(diab_cc),24,15,8,4,1,.80)
DemoData.loc[diab,'delta_diab'] = dist_builder(len(diab),17,11,5,2,1,.80)

#type cast to timedelta days
DemoData['delta_diab_mcc'] = pd.to_timedelta(DemoData['delta_diab_mcc'], unit='d')
DemoData['delta_diab_cc'] = pd.to_timedelta(DemoData['delta_diab_cc'], unit='d')
DemoData['delta_diab'] = pd.to_timedelta(DemoData['delta_diab'], unit='d')

#Create new Discharge dates from timedeltas
DemoData.loc[diab_mcc,'Disch_DT'] = DemoData.loc[diab_mcc,'delta_diab_mcc'] + DemoData.loc[diab_mcc,'Admit_DT']
DemoData.loc[diab_cc,'Disch_DT'] = DemoData.loc[diab_cc,'delta_diab_cc'] + DemoData.loc[diab_cc,'Admit_DT']
DemoData.loc[diab,'Disch_DT'] = DemoData.loc[diab,'delta_diab'] + DemoData.loc[diab,'Admit_DT']

#ENHANCE THIS LATER FOR TRUE READMITS BASED OFF MANY TO 1 RELATIONSHIP OF MRN TO ENCOUNTER
#create unique MRN for every row; if you want true reAdmits adjust total to <total
mrn = []
mrn = random.sample(range(1000000, 9999999), length_df)
DemoData['MRN'] = mrn

#create list of unique months
DemoData['Admit_month'] = DemoData['Admit_DT'].dt.month
months = DemoData['Admit_month'].unique().tolist()

#Readmits flag
#plants Readmitted flag @ specified % of population on monthly basis
for month in months:
    test_frac2 = random.uniform(.07,.15)
    indices = DemoData[DemoData['Admit_month']==month].sample(frac = test_frac2).index.tolist()
    DemoData.loc[indices,'Readmitted']='Yes'

#grab readmits
readmits = DemoData[DemoData['Readmitted']=='Yes'].index.tolist()

#create LOS for readmits
#DemoData.loc[diab_mcc,'delta_diab_mcc'] = dist_builder(len(diab_mcc),30,18,12,8,1,.80)
DemoData.loc[readmits,'delta_readmits'] = dist_builder(len(readmits),30,18,12,8,1,.80)


#type cast to timedelta days
DemoData['delta_readmits'] = pd.to_timedelta(DemoData['delta_readmits'], unit='d')

#Create new Discharge dates for readmits from timedeltas
DemoData.loc[readmits,'Disch_DT'] = DemoData.loc[readmits,'delta_readmits'] + DemoData.loc[readmits,'Admit_DT']

#inflate costs for readmits by 15%
DemoData.loc[readmits,'Charge_perDay_tmp'] = DemoData.loc[readmits,'Charge_perDay_tmp'] * 1.08

#clear out any discharges beyond current date
DemoData.ix[DemoData.Disch_DT >= today,'Disch_DT'] = np.NaN

#set temp discharge to today to get total charges thru current date for patients not discharged yet; still in hospital
DemoData['Disch_DT_tmp2'] = DemoData['Disch_DT']
DemoData.ix[DemoData.Disch_DT >= today,'Disch_DT_tmp2'] = today

#calc total charges based off LOS_out_tmp x Charge_perDay_tmp
DemoData['LOS_out_tmp'] = pd.to_datetime(DemoData['Disch_DT_tmp2']) - pd.to_datetime(DemoData['Admit_DT'])
DemoData['LOS_out_tmp'] = DemoData['LOS_out_tmp'].dt.days + 1
DemoData['TotalCharges2'] = DemoData['LOS_out_tmp'] * DemoData['Charge_perDay_tmp']
DemoData['Total Charges'] = DemoData['TotalCharges2']

#remove legacy fields
fields = ['TotalCharges2','From Day', 'LOS_tmp', 'Charge_perDay_tmp' , 'Disch Stat', 'F33', 'delta_readmits', 'Admit_month', 'Uniqueid','From Date','To Date','Length of Stay','Unique ID Join','To Day','Zip Lon','Zip Lat','Miles From Provider','delta_diab_mcc','delta_diab_cc','delta_diab','Disch_DT_tmp2','LOS_out_tmp']
DemoData = DemoData.drop(fields, axis=1)

uniqueDiabetes22 = DemoData[DemoData['DRG Text'].str.contains('DIABETES')==True]['MRN'].tolist() 

#Create list of indeces filtered where Admit date is >10 days old, but <90 days
start = today - dt.timedelta(days = 90)
end = today - dt.timedelta(days = 10)
#index_tmp = rawDF1[(rawDF1['Admit']>=start)&(rawDF1['Admit']<end)].index.tolist()
ID_tmp = DemoData[(DemoData['Admit_DT']>=start)&(DemoData['Admit_DT']<end)]['MRN'].tolist()

#return set with ID's common to both <90days and DRG=diabetes
x=set(uniqueDiabetes22).intersection(ID_tmp)

#randomly select labs for x number of diabetes patients (<90days and DRG=diabetes)
x_1 = random.sample(x,len(x))
len(x_1)

#Give it same name for Tableau "smart" join
df2['MRN']=pd.Series(x_1)
df2_trim = df2[0:(len(x)-1)]
df2 = df2_trim

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















