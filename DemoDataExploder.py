import pandas as pd
import datetime as dt
import numpy as np
import random

#Read in 'Inpatient' and 'Lab Results' data
file1 = '/Users/jcraycraft/Dropbox/Work/PreSales/Marketing/2017_HIMSS/DiabetesReAdmitDemo/Inpatient Data (RMTD) Extract.csv'
file2 = '/Users/jcraycraft/Dropbox/Work/PreSales/Marketing/2017_HIMSS/DiabetesReAdmitDemo/HCPyDiabetesClinical_excludeNone.csv'
file3 = '/Users/jcraycraft/Dropbox/Work/PreSales/Marketing/2017_HIMSS/DiabetesReAdmitDemo/superstore.csv'
# Read CSV into dataframe (two files)
df1 = pd.read_csv(file1, encoding='utf-16', sep='\t', error_bad_lines=False)
df2 = pd.read_csv(file2)
df3 = pd.read_csv(file3)

#today's date
today = pd.to_datetime('today')
#date -1460 days equals 4 years from Today
start_dates = today - dt.timedelta(days = 1460)
#create list that includes every day over last 4 years (1460 days)
df_dates3 = pd.date_range(start=start_dates, end=today, freq = 'D').tolist()
out_df = pd.DataFrame()
final_df = pd.DataFrame()
outData_df = pd.DataFrame()


#this works; just can't access object in current format (timestamp)
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


indy_dict = {'Mon':[0,7,14,21,28],'Tues':[1,8,15,22,29],'Wed':[2,9,16,23,30],'Thur':[3,10,17,24,31],'Fri':[4,11,18,25,32],'Sat':[5,12,19,26,33],'Sun':[6,13,20,27,34]}
avgVar_dict = {'Mon':[260,45],'Tues':[277,41],'Wed':[250,20],'Thur':[230,30],'Fri':[223,35],'Sat':[150,20],'Sun':[145,20]}
avgVar_dict2 = {'Mon':[1,45],'Tues':[2,41],'Wed':[3,20],'Thur':[4,30],'Fri':[5,35],'Sat':[6,20],'Sun':[7,20]}
        
 

#need YoY growth indexed

growth = [[1,.03],[1.15,.05],[1.175,.07],[1.20,.09],[1.225,.10]]
growth[0][0]=1
growth[0][1]=.03

#cycle thru all the weekdays
#start with first weekday = Monday, iterate across all years 
#then for each day blow out the rows using multipliers based off the dictionaries
  
#USE LATER FOR ITERATING ACROSS DICTIONARIES    
#create n rows for specified date
#for (k,v), (k2,v2) in zip(avgVar_dict.items(), indy_dict.items()):
#prove first attempt with today's date; then improve with other dates

#declare global objects

out_df = pd.DataFrame() 
out_df2 = pd.DataFrame()

#static n, but adjust in final version
#n = 25

ct_1=0
ct_2=0
ct_3=0
ct_4=0





#1
for (k,v), (k2,v2) in zip(avgVar_dict2.items(), indy_dict.items()):
    ct_1+=1
    print('#1: ',ct_1)
    #use k2,v2 index to select slice of dates
    #pass to tmpDates
    tmp_iterator = v2
    #print(tmp_iterator)
    #for tmp_item in tmp_iterator:
    #2
    sub_df = pd.DataFrame()    
    
    for idx, tmp_item in enumerate(tmp_iterator): 
        ct_2+=1
        print('#2: ',ct_2)
        #tmpDates = final[0][v2[tmp_item]]
        tmpDates = final[0][v2[idx]]
        #print(tmpDates)
        #v[idx] is number of rows
        #print(v[0],v[1])
        #static n, but adjust in final version
        n = 2
        #dynamically set n
        #n = v[0]
        #3
        tmp_df3 = pd.DataFrame()
        for date in tmpDates:
            ct_3+=1
            print('#3: ',ct_3)
            print(date)
            #4
            tmp_df1 = pd.DataFrame()
            tmp_df2 = pd.DataFrame()
            for i in range(n):
                ct_4+=1
                print('#4: ',ct_4)
                #5
                #random index
                tmp_index = random.randint(0, 20000)
                #select row from source data using random index
                tmp_df1 = df1.ix[tmp_index]
                #append onto dataframe and build temp df for given date
                tmp_df2 = tmp_df2.append(tmp_df1)
            tmp_df3 = tmp_df3.append(tmp_df2)
            #set date for given date across all rows in temp df
            tmp_df3['date'] = date
        #append temp df onto output df
        sub_df = sub_df.append(tmp_df3)
    out_df = out_df.append(sub_df)
out_df2 = out_df2.append(out_df)      



#output file
out_df2.to_csv('out2_dfApril1_2.csv', index = False)


