
import pandas as pd
import datetime as dt
import numpy as np
import random

#Read in 'Inpatient' and 'Lab Results' data
file1 = '/Users/jcraycraft/Dropbox/Work/PreSales/Marketing/2017_HIMSS/DiabetesReAdmitDemo/Inpatient Data (RMTD) Extract.csv'
file2 = '/Users/jcraycraft/Dropbox/Work/PreSales/Marketing/2017_HIMSS/DiabetesReAdmitDemo/HCPyDiabetesClinical_excludeNone.csv'
# Read CSV into dataframe (two files)
df1 = pd.read_csv(file1, encoding='utf-16', sep='\t', error_bad_lines=False)
df2 = pd.read_csv(file2)

#today's date
today = pd.to_datetime('today')
#date -1460 days equals 4 years from Today
start_dates = today - dt.timedelta(days = 1460)
#create list that includes every day over last 4 years (1460 days)
df_dates3 = pd.date_range(start=start_dates, end=today, freq = 'D').tolist()
out_df = pd.DataFrame()
final_df = pd.DataFrame()


#prefilter df_dates3 list into seperate lists of Mondays, Tuesdays, Wed's, etc. 7 lists, each containing all dates for that weekday
#then pass to ITERATOR_DAY across each weekday pass in dates, pass in avg, pass in variability
#http://stackoverflow.com/questions/3013449/list-filtering-list-comprehension-vs-lambda-filter


weekdays = [0,1,2,3,4,5,6]
datesByWeekday = []
for day in weekdays:
    result = filter(lambda x: x.weekday()==day, df_dates3)
    datesByWeekday.append(result)


#iterate thru grab the avg & range for each weekday
weekdays = [[260,45],[277,41],[250,20],[230,30],[223,35],[150,20],[145,20]]
for idx, weekday in enumerate(weekdays):




    #ITERATOR_DAY
    #iterate thru each day in the df_dates3 list, add 150 random rows
    #sub_df = pd.DataFrame()
    sub_df = pd.DataFrame()
    for date in datesByWeekday[idx]:
        n = weekday[0] + random.randint(-weekday[1],weekday[1])
        tmp_df2 = pd.DataFrame()
        for i in range(n):
            tmp_index = random.randint(0, 20000)
            tmp_df1 = df1.ix[tmp_index]
            tmp_df2 = tmp_df2.append(tmp_df1)
        tmp_df2['date'] = date
        sub_df = sub_df.append(tmp_df2)
    out_df = out_df.append(sub_df)
final_df = final_df.append(out_df)



   

